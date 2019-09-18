"""
Module for common functions and classes.
"""

import re
from os import getpid, stat, remove
from os.path import isfile
from enum import Enum
from typing import Iterable
from ensure import ensure_annotations


@ensure_annotations
def ignore_append(ignored: str):
    """
    Append a file path to a file with all ignored files.
    """
    with open(f'{getpid()}_ignored.txt', 'a') as out:
        out.write(ignored)
        out.write('\n')


@ensure_annotations
def oversized_file(path: str, limit: int) -> bool:
    """
    Check if a specified file is within a desired limit in bytes.
    """
    result = False
    if limit and isfile(path):
        result = stat(path).st_size > limit
    return result


@ensure_annotations
def pattern_exclude(value: str, patterns: list) -> bool:
    """
    Exclude (True) a value if it contains any of the patterns.
    """
    return any([exc in value for exc in patterns])


@ensure_annotations
def regex_exclude(value: str, regexes: list) -> bool:
    """
    Exclude (True) a value if any of the regex pattern applies.
    """
    return any([re.search(exc, value) for exc in regexes])


@ensure_annotations
def remove_except_oldest(files: Iterable):
    """
    Remove all files from list except the single oldest one.
    """
    for candidate in files:
        # oldest == smallest timestamp
        without_oldest = sorted(
            candidate, key=lambda item: stat(item).st_mtime
        )[1:]
        for file in without_oldest:
            remove(file)


@ensure_annotations
def remove_except_newest(files: Iterable):
    """
    Remove all files from list except the single newest one.
    """
    for candidate in files:
        # reverse for oldest
        without_newest = sorted(
            candidate, key=lambda item: stat(item).st_mtime, reverse=True
        )[1:]
        for file in without_newest:
            remove(file)


class Hasher(Enum):
    """
    Enum to switch between multiple hashing algorithms.
    """
    MD5 = 1
    SHA256 = 2
    BLAKE2 = 3
