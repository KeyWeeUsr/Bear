"""
Test hashing of specific file contents.
"""

from unittest import TestCase, main

from bear import hasher


class HashCase(TestCase):
    def test_hash_word(self):
        self.assertEqual(
            '098f6bcd4621d373cade4e832627b4f6',
            hasher('test'.encode('utf-8'))
        )


if __name__ == '__main__':
    main()
