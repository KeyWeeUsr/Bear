"""
Module for hashing-related functions.
"""

import logging
import traceback
from os import getpid
from ensure import ensure_annotations

from bear.common import ignore_append, Hasher

LOG = logging.getLogger(__name__)


@ensure_annotations
def hash_text(inp: bytes, hasher: Hasher) -> str:
    """
    Hash simple string of text.
    """
    result = None
    if hasher == Hasher.MD5:
        from hashlib import md5
        result = md5(inp).hexdigest()
    elif hasher == Hasher.SHA256:
        from hashlib import sha256
        result = sha256(inp).hexdigest()
    elif hasher == Hasher.BLAKE2:
        from hashlib import blake2b
        result = blake2b(inp).hexdigest()
    return result


@ensure_annotations
def hash_file(path: str, hasher: Hasher) -> str:
    """
    Open a file, read its contents and return MD5 hash.
    """
    result = ''
    try:
        with open(path, 'rb') as file:
            contents = file.read()
        result = hash_text(inp=contents, hasher=hasher)
    except PermissionError:
        LOG.critical(
            'Could not open %s due to permission error! %s',
            path, traceback.format_exc()
        )
        ignore_append(path)
    except FileNotFoundError:
        LOG.warning('Could not find file %s! Did you delete it?', path)
        ignore_append(path)
    except OSError:
        LOG.critical('Could not open %s! %s', path, traceback.format_exc())
        ignore_append(path)
    return result


def hash_files(files: list, hasher: Hasher, master_pid: int = None) -> dict:
    """
    Hash each of the file in the list.

    In case of a MemoryError (limitation of e.g. 32-bit Python)
    write out the file names in separate .txt files per PID
    of the process used for hashing.

    Note: master_pid should have a default in case of running out of MP,
          and use master's PID so that master can recognize slave processes'
          files after the slaves in the Pool are terminated.
    """

    hashfiles = {}
    files_len = len(files)
    partial_file = f"bear_m{master_pid}_s{getpid()}_hashes.txt"

    # safe-check in case the name changes in the future to prevent
    # creating files that won't be deleted by master process
    assert f"bear_m{master_pid}_" in partial_file
    assert f"_hashes.txt" in partial_file

    for idx, fname in enumerate(files):
        LOG.debug('Hashing %d / %d', idx + 1, files_len)

        try:
            fhash = hash_file(path=fname, hasher=hasher)
            if not fhash:
                continue
            with open(partial_file, "a") as file:
                file.write(f"{fhash}\t{fname}\n")
            if fhash not in hashfiles:
                hashfiles[fhash] = [fname]
            else:
                hashfiles[fhash].extend([fname])
        except MemoryError:
            LOG.critical(
                'Not enough memory while hashing %s, skipping.', fname
            )
            ignore_append(fname)

    return hashfiles
