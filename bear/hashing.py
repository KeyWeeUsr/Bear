"""
Module for hashing-related functions.
"""

import logging
import traceback
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


def hash_files(files: list, hasher: Hasher) -> dict:
    """
    Hash each of the file in the list.

    In case of a MemoryError (limitation of e.g. 32-bit Python)
    write out the file names in separate .txt files per PID
    of the process used for hashing.
    """

    hashfiles = {}
    files_len = len(files)

    for idx, fname in enumerate(files):
        LOG.debug('Hashing %d / %d', idx + 1, files_len)

        try:
            fhash = hash_file(path=fname, hasher=hasher)
            if not fhash:
                continue
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
