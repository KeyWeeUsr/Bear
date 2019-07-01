"""
Test hashing of specific file contents.
"""

from unittest import TestCase, main
from tempfile import mkstemp
from os import remove
from bear.common import Hasher
from bear.hashing import hash_text, hash_file


class HashCase(TestCase):
    """
    Test hashing functions.
    """

    def test_hash_word_md5(self):
        """
        Test hashing a string.
        """
        self.assertEqual(
            '098f6bcd4621d373cade4e832627b4f6',
            hash_text(inp='test'.encode('utf-8'), hasher=Hasher.MD5)
        )

    def test_hash_file_md5(self):
        """
        Test hashing bytes of a file.
        """
        base = b'\xecO\xda\xad\x12\x85\xa1\xe1\xbd\xb7\xf1'
        (desc, path) = mkstemp(text=False)
        with open(desc, 'wb') as file:
            file.write(base)
        hashed = hash_file(path=path, hasher=Hasher.MD5)
        remove(path)
        self.assertEqual('7972892f41d1b98a71d9583b83267d8b', hashed)


if __name__ == '__main__':
    main()
