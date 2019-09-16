"""
Module for context and configuration grouping.
"""

from argparse import Namespace
from ensure import ensure_annotations
from bear.common import Hasher


class Context:
    """
    Object holding info about the application's configuration passed into
    functions or other classes to keep the code clean of the global variables
    and unnecessary 2+ cluttering function parameters.
    """
    # pylint: disable=too-few-public-methods

    jobs: int
    output: str
    exclude: list
    exclude_regex: list
    verbose: int
    quiet: bool
    files: list
    traverse: list
    hash: list
    duplicates: list
    version: bool
    community: bool
    keep_oldest: bool
    keep_newest: bool
    md5: bool
    blake2: bool
    sha256: bool
    max_size: int
    load_hashes: list
    hasher: Hasher

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
            max_size=0,
            load_hashes=[],
            hasher=Hasher.MD5
        )

        for key, value in vars(args).items():
            assert isinstance(value, self.__annotations__[key]), (
                f"{key}: {type(value)} should be {self.__annotations__[key]}"
            )
            defaults[key] = value

        for conf, value in defaults.items():
            assert isinstance(value, self.__annotations__[conf]), (
                f"{conf}: {type(value)} should be {self.__annotations__[conf]}"
            )
            setattr(self, conf, value)

        # custom field setters
        self.hasher = self.get_hasher()

    @ensure_annotations
    def get_hasher(self) -> Hasher:
        """
        Get non-MD5 hasher if desired.
        """
        if self.blake2:
            result = Hasher.BLAKE2
        elif self.sha256:
            result = Hasher.SHA256
        elif self.md5:
            result = Hasher.MD5
        return result
