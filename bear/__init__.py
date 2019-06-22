"""
Main file for the Bear package.
"""

from hashlib import md5

VERSION = '0.0.2'


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
