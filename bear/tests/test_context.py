"""
Text Context object.
"""

from unittest import TestCase, main
from argparse import Namespace

from ensure import EnsureError

from bear.common import Hasher
from bear.context import Context


class ContextCase(TestCase):
    """
    Test Context object.
    """

    def test_hasher_md5(self):
        """
        Test getting Hasher from Context configuration.
        """
        ctx = Context(Namespace(md5=True, blake2=False, sha256=False))
        self.assertEqual(ctx.hasher, Hasher.MD5)

    def test_hasher_sha256(self):
        """
        Test getting Hasher from Context configuration.
        """
        ctx = Context(Namespace(md5=False, blake2=False, sha256=True))
        self.assertEqual(ctx.hasher, Hasher.SHA256)

    def test_hasher_blake2(self):
        """
        Test getting Hasher from Context configuration.
        """
        ctx = Context(Namespace(md5=False, blake2=True, sha256=False))
        self.assertEqual(ctx.hasher, Hasher.BLAKE2)

    def test_hasher_invalid_setup(self):
        """
        Test getting Hasher from Context configuration.
        """
        with self.assertRaises(EnsureError):
            # invalid setup, context is None which is mistyped, therefore fails
            Context(Namespace(md5=False, blake2=False, sha256=False))


if __name__ == '__main__':
    main()
