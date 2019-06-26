"""
Module for output-related functions.
"""
import logging
from os import walk, cpu_count
from os.path import exists, join, abspath, realpath
from multiprocessing import Pool
from datetime import datetime
from ensure import ensure_annotations

from bear.hashing import hash_files

LOG = logging.getLogger(__name__)


@ensure_annotations
def find_files(folder: str) -> list:
    """
    Walk a folder to create a flat list of files.
    """

    result = []

    if not exists(folder):
        LOG.critical('Folder %s does not exist! Skipping.', folder)
        return result

    result = [
        join(name, fname)
        for name, folder, files in walk(folder)
        for fname in files
    ]
    return result


@ensure_annotations
def filter_files(files: dict) -> dict:
    """
    Filter out hashes with only single file connected to them to prevent
    having all of the file hashes even if the files are not duplicated.
    """

    return {key: value for key, value in files.items() if len(value) > 1}


@ensure_annotations
def find_duplicates(folders: list, processes: int = 1) -> dict:
    """
    Find duplicates in multiple folders with multiprocessing.
    """
    # get user specified or max jobs
    processes = processes if processes != 0 else cpu_count()

    # traverse the input folders
    found = [find_files(abspath(realpath(folder))) for folder in folders]
    files = [file for file_list in found for file in file_list]
    files_len = len(files)
    chunk_size = int(files_len // processes)

    # hash chunks of flat list files
    with Pool(processes=processes) as pool:
        results = pool.map(
            hash_files, [
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
def output_duplicates(hashes: dict, out: str = None):
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
