"""
Test hashing of specific file contents.
"""

from unittest import TestCase, main
from tempfile import mkstemp
from os import remove
from bear import hash_text, hash_file


class HashCase(TestCase):
    """
    Test hashing functions.
    """

    def test_hash_word(self):
        """
        Test hashing a string.
        """
        self.assertEqual(
            '098f6bcd4621d373cade4e832627b4f6',
            hash_text('test'.encode('utf-8'))
        )

    def test_hash_file(self):
        """
        Test hashing bytes of a file.
        """
        base = b'\xecO\xda\xad\x12\x85\xa1\xe1\xbd\xb7\xf1'
        (desc, path) = mkstemp(text=False)
        with open(desc, 'wb') as file:
            file.write(base)
        hashed = hash_file(path)
        remove(path)
        self.assertEqual('7972892f41d1b98a71d9583b83267d8b', hashed)


if __name__ == '__main__':
    main()
