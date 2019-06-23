"""
Test file and folder manipulation.
"""

from unittest import TestCase, main
from bear import find_files


class HashCase(TestCase):
    """
    Test file and folder manipulation functions.
    """

    def test_find_files_nonexisting(self):
        """
        Test calling bear.find_files on non-existing folder.
        """
        with self.assertRaises(Exception):
            find_files('_' * 30)


if __name__ == '__main__':
    main()
