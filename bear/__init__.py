"""
Main file for the Bear package.
"""

import logging
from hashlib import md5
from os import walk, cpu_count, getpid
from os.path import exists, join, abspath, realpath
from multiprocessing import Pool
from datetime import datetime

VERSION = '0.1.0'
LOG = logging.getLogger(__name__)


def hash_text(inp):
    """
    Hash simple string of text.
    """
    return md5(inp).hexdigest()


def hash_file(path):
    """
    Open a file, read its contents and return MD5 hash.
    """
    with open(path, 'rb') as file:
        contents = file.read()
    return hash_text(contents)


def find_files(folder):
    """
    Walk a folder to create a flat list of files.
    """

    if not exists(folder):
        raise Exception('Folder does not exist')

    return [
        join(name, fname)
        for name, folder, files in walk(folder)
        for fname in files
    ]


def hash_files(files):
    """
    Hash each of the file in the list.

    In case of a MemoryError (limitation of e.g. 32-bit Python)
    write out the file names in separate .txt files per PID
    of the process used for hashing.
    """

    hashfiles = {}
    files_len = len(files)

    def ignore_append(ignored):
        """
        Append a file path to a file with all ignored files.
        """
        with open(f'{getpid()}_ignored.txt', 'a') as out:
            out.write(fname)
            out.write('\n')

    for idx, fname in enumerate(files):
        LOG.debug('Hashing %d / %d', idx + 1, files_len)

        try:
            try:
                fhash = hash_file(fname)
                if fhash not in hashfiles:
                    hashfiles[fhash] = [fname]
                else:
                    hashfiles[fhash].extend([fname])
            except MemoryError:
                LOG.critical(
                    'Not enough memory while hashing %s, skipping.', fname
                )
                ignore_append(fname)
        except FileNotFoundError:
            LOG.warning('File %s not found, skipping.', fname)
            ignore_append(fname)

    return hashfiles


def filter_files(files):
    """
    Filter out hashes with only single file connected to them to prevent
    having all of the file hashes even if the files are not duplicated.
    """

    return {key: value for key, value in files.items() if len(value) > 1}


def find_duplicates(folders, processes=1):
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


def output_duplicates(hashes, out=None):
    """
    Output a simple structure for the duplicates:

    <hash>:
    \t<path>
    \t<path>
    ...
    """
    stamp = str(datetime.now()).replace(':', '_').replace(' ', '_')
    out = f'{stamp}_duplicates.txt' if not out else out

    with open(out, 'wb') as out:
        for key, val in hashes.items():
            if not isinstance(key, bytes):
                key = key.encode('utf-8', 'ignore')

            # hash
            out.write(key)
            out.write(b'\n')

            # tabbed file path(s), exclude invalid characters
            for item in val:
                out.write(b'\t' + str(item).encode('utf-8', 'ignore') + b'\n')

            # separator
            out.write(b'\n\n')
