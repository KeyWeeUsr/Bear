"""
Main file for the Bear package.
"""

from hashlib import md5


def hasher(inp):
    return md5(inp).hexdigest()
