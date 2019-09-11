"""
Module for output-related functions.
"""
import re
import logging
from os import walk, cpu_count
from os.path import exists, join, abspath, realpath
from multiprocessing import Pool
from datetime import datetime
from functools import partial
from ensure import ensure_annotations

from bear.common import Hasher
from bear.hashing import hash_files

LOG = logging.getLogger(__name__)


@ensure_annotations
def find_files(
        # pylint: disable=dangerous-default-value
        folder: str, exclude: list = [], exclude_regex: list = []
) -> list:
    """
    Walk a folder to create a flat list of files.
    """

    result = []

    if not exists(folder):
        LOG.critical('Folder %s does not exist! Skipping.', folder)
        return result

    def _in_excluded(value):
        return any([exc in value for exc in exclude])

    def _in_excluded_regex(value):
        return any([re.search(exc, value) for exc in exclude_regex])

    for name, _, files in walk(folder):
        for fname in files:
            path = join(name, fname)

            if _in_excluded(path):
                continue
            if _in_excluded_regex(path):
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
def find_duplicates(
        # pylint: disable=dangerous-default-value
        folders: list, hasher: Hasher, processes: int = 1,
        exclude: list = [], exclude_regex: list = []
) -> dict:
    """
    Find duplicates in multiple folders with multiprocessing.
    """
    # get user specified or max jobs
    processes = processes if processes != 0 else cpu_count()

    # traverse the input folders
    found = [
        find_files(
            folder=abspath(realpath(folder)),
            exclude=exclude, exclude_regex=exclude_regex
        )
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
    with Pool(processes=processes) as pool:
        results = pool.map(
            # because starmap uses positional args which will become unsafer
            # on each change to the workflow (i.e. more work to find bugs)
            partial(hash_files, hasher=hasher), [
                # chunk files into smaller lists
                files[idx: idx + chunk_size]
                for idx in range(files_len)
                if idx % chunk_size == 0
            ]
        )

    # join values from all jobs
    files = {}
    for result in results:
        for key, val in result.items():
            if key not in files:
                files[key] = val
            else:
                files[key].extend(val)

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
