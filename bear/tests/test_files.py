"""
Test file and folder manipulation.
"""

from unittest import TestCase, main
from unittest.mock import patch
from os.path import join

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

    def test_find_files(self):
        """
        Test hashing a string.
        """
        mocked_walk = [(
            'bear', [
                'emptyfolder', 'tests', '__pycache__'
            ], [
                '__main__.py', '__init__.py'
            ]
        ), (
            'bear/emptyfolder', [], []
        ), (
            'bear/tests', ['__pycache__'], [
                'test_files.py', 'test_main.py',
                '__init__.py', 'test_hash.py'
            ]
        ), (
            'bear/tests/__pycache__', [], [
                'test_files.cpython-37.pyc', 'test_hash.cpython-37.pyc',
                '__init__.cpython-37.pyc', 'test_main.cpython-37.pyc'
            ]
        ), (
            'bear/__pycache__', [], [
                '__init__.cpython-37.pyc', '__main__.cpython-37.pyc'
            ]
        )]

        expected = [
            join(name, fname)
            for name, folder, files in mocked_walk
            for fname in files
        ]

        patch_walk = patch('bear.walk', return_value=mocked_walk)
        with patch_walk, patch('bear.exists', return_value=True):
            self.assertEqual(find_files('_' * 30), expected)


if __name__ == '__main__':
    main()
