"""
Module for common functions and classes.
"""

from os import getpid
from enum import Enum
from ensure import ensure_annotations


@ensure_annotations
def ignore_append(ignored: str):
    """
    Append a file path to a file with all ignored files.
    """
    with open(f'{getpid()}_ignored.txt', 'a') as out:
        out.write(ignored)
        out.write('\n')


class Hasher(Enum):
    """
    Enum to switch between multiple hashing algorithms.
    """
    MD5 = 1
    SHA256 = 2
    BLAKE2 = 3
