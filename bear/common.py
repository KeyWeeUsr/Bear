"""
Module for common functions and classes.
"""

from os import getpid
from ensure import ensure_annotations


@ensure_annotations
def ignore_append(ignored: str):
    """
    Append a file path to a file with all ignored files.
    """
    with open(f'{getpid()}_ignored.txt', 'a') as out:
        out.write(ignored)
        out.write('\n')
