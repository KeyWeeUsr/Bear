"""
Module for hashing-related functions.
"""
import logging
import traceback
from hashlib import md5
from ensure import ensure_annotations

from bear.common import ignore_append

LOG = logging.getLogger(__name__)


@ensure_annotations
def hash_text(inp: bytes) -> str:
    """
    Hash simple string of text.
    """
    return md5(inp).hexdigest()


@ensure_annotations
def hash_file(path: str) -> str:
    """
    Open a file, read its contents and return MD5 hash.
    """
    result = ''
    try:
        with open(path, 'rb') as file:
            contents = file.read()
        result = hash_text(contents)
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


def hash_files(files: list) -> dict:
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
            fhash = hash_file(fname)
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
