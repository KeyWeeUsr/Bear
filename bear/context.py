"""
Module for context and configuration grouping.
"""

from argparse import Namespace
from ensure import ensure_annotations


class Context:
    """
    Object holding info about the application's configuration passed into
    functions or other classes to keep the code clean of the global variables
    and unnecessary 2+ cluttering function parameters.
    """

    @ensure_annotations
    def __init__(self, args: Namespace):
        defaults = dict(
            jobs=1,
            output='',
            exclude=[],
            exclude_regex=[],
            verbose=0,
            quiet=False,
            files=None,
            traverse=None,
            hash=None,
            duplicates=None,
            version=False,
            community=False,
            keep_oldest=False,
            keep_newest=False,
            md5=True,
            blake2=False,
            sha256=False,
            max_size=0
        )

        for key, value in vars(args).items():
            defaults[key] = value

        for conf, value in defaults.items():
            setattr(self, conf, value)
