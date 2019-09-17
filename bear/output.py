"""
Module for output-related functions.
"""

import logging
from os import walk, cpu_count, getpid, remove, listdir
from os.path import exists, join, abspath, realpath
from multiprocessing import Pool
from datetime import datetime
from functools import partial
from ensure import ensure_annotations

from bear.common import (
    Hasher, oversized_file, regex_exclude, pattern_exclude
)
from bear.hashing import hash_files
from bear.context import Context

LOG = logging.getLogger(__name__)


@ensure_annotations
def find_files(ctx: Context, folder: str) -> list:
    """
    Walk a folder to create a flat list of files.
    """

    result = []

    if not exists(folder):
        LOG.critical('Folder %s does not exist! Skipping.', folder)
        return result

    for name, _, files in walk(folder):
        for fname in files:
            path = join(name, fname)

            if pattern_exclude(value=path, patterns=ctx.exclude):
                continue
            if regex_exclude(value=path, regexes=ctx.exclude_regex):
                continue
            if oversized_file(path=path, limit=ctx.max_size):
                continue

            result.append(path)

    return result


@ensure_annotations
def filter_files(files: dict) -> dict:
    """
    Filter out hashes with only single file connected to them to prevent
    having all of the file hashes even if the files are not duplicated.
    """

    return {key: value for key, value in files.items() if len(value) > 1}


@ensure_annotations
def find_duplicates(ctx: Context, hasher: Hasher) -> dict:
    """
    Find duplicates in multiple folders with multiprocessing.
    """
    # get user specified or max jobs
    folders = ctx.duplicates
    processes = ctx.jobs if ctx.jobs != 0 else cpu_count()

    # traverse the input folders
    found = [
        find_files(ctx=ctx, folder=abspath(realpath(folder)))
        for folder in folders
    ]
    files = [file for file_list in found for file in file_list]
    files_len = len(files)
    chunk_size = int(files_len // processes)
    if chunk_size == 0:
        # watch out for zero division
        LOG.critical((
            'Zero chunk size for files: %d, processes: %d! '
            'Using 1 as default.'
        ), files_len, processes)
        chunk_size = 1

    # hash chunks of flat list files
    master_pid = getpid()
    with Pool(processes=processes) as pool:
        results = pool.map(
            # because starmap uses positional args which will become unsafer
            # on each change to the workflow (i.e. more work to find bugs)
            partial(hash_files, hasher=hasher, master_pid=master_pid), [
                # chunk files into smaller lists
                files[idx: idx + chunk_size]
                for idx in range(files_len)
                if idx % chunk_size == 0
            ]
        )

    # load saved duplicates if any, otherwise {}
    files = load_duplicates_from_hashfiles(ctx=ctx)

    # join values from all jobs
    for result in results:
        for key, val in result.items():
            if key not in files:
                files[key] = val
            else:
                files[key].extend(val)

    # Pool terminated, results properly joined (no out of memory exc)
    # remove partial results as these are not needed anymore
    for file in listdir("."):
        if f"bear_m{master_pid}_" not in file:
            continue
        if "_hashes.txt" not in file:
            continue
        remove(file)

    # filter out non-duplicates
    return filter_files(files)


@ensure_annotations
def load_duplicates_from_hashfiles(ctx: Context) -> dict:
    """
    Find duplicates from previous temporary output (mainly if MP deadlocked).
    """
    # join values from hashfiles
    files = {}
    for hashfile in ctx.hashfiles:
        with open(hashfile) as file:
            lines = file.readlines()
        for line in lines:
            # pylint: disable=redefined-builtin
            hash, path = line.split("\t")
            path = path.strip()
            if hash not in files:
                files[hash] = [path]
            else:
                files[hash].append(path)

    # filter out non-duplicates
    return filter_files(files)


@ensure_annotations
def output_duplicates(hashes: dict, out: str = ''):
    """
    Output a simple structure for the duplicates:

    <hash>:
    \t<path>
    \t<path>
    ...
    """
    stamp = str(datetime.now()).replace(':', '_').replace(' ', '_')
    out = f'{stamp}_duplicates.txt' if not out else out

    with open(out, 'wb') as fout:
        for key, val in hashes.items():
            if not isinstance(key, bytes):
                key = key.encode('utf-8', 'ignore')

            # hash
            fout.write(key)
            fout.write(b'\n')

            # tabbed file path(s), exclude invalid characters
            for item in val:
                fout.write(b'\t' + str(item).encode('utf-8', 'ignore') + b'\n')

            # separator
            fout.write(b'\n\n')
