"""
Main file for the Bear package.
"""

from hashlib import md5
from os import walk
from os.path import exists, join

VERSION = '0.0.4'


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
    """

    hashfiles = {}
    files_len = len(files)

    def ignore_append(ignored):
        """
        Append a file path to a file with all ignored files.
        """
        with open(f'ignored.txt', 'a') as out:
            out.write(fname)
            out.write('\n')

    for idx, fname in enumerate(files):
        print(f'Hashing {idx + 1} / {files_len}')

        try:
            try:
                fhash = hash_file(fname)
                if fhash not in hashfiles:
                    hashfiles[fhash] = [fname]
                else:
                    hashfiles[fhash].extend([fname])
            except MemoryError:
                ignore_append(fname)
        except FileNotFoundError:
            ignore_append(fname)

    return hashfiles


def filter_files(files):
    """
    Filter out hashes with only single file connected to them to prevent
    having all of the file hashes even if the files are not duplicated.
    """

    return {key: value for key, value in files.items() if len(value) > 1}
