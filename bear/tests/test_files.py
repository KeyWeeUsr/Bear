"""
Test file and folder manipulation.
"""

from unittest import TestCase, main
from unittest.mock import patch, MagicMock, call
from os.path import join

from bear import find_files, filter_files, hash_files, ignore_append


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

    def test_filter_files(self):
        """
        Test removing duplicates from dictionary of hashes + files.
        """
        hashes = {
            'empty': [], 'original': ['file'],
            'orig+dup': ['file', 'duplicate'],
            'orig+2xdup': ['file', 'duplicate2']
        }
        self.assertEqual(
            filter_files(hashes), dict(
                item for item in hashes.items()
                if item[0] not in ('empty', 'original')
            )
        )

    @staticmethod
    def test_ignore_append():
        """
        Test writing ignored path to a file.
        """
        pid = 12345
        patch_pid = patch('bear.getpid', return_value=pid)

        file_obj = MagicMock()
        mocked_open_inst = MagicMock(
            __enter__=MagicMock(return_value=file_obj)
        )
        patch_open = patch(
            'builtins.open', return_value=mocked_open_inst
        )

        with patch_pid, patch_open as mocked_open:
            ignore_append('lalala')

            mocked_open.assert_called_once_with(f'{pid}_ignored.txt', 'a')

            file_obj.write.assert_has_calls([call('lalala'), call('\n')])

    @staticmethod
    def test_hash_files_memoryerror():
        """
        Test hashing a list of files returning MemoryError on file.read().
        """
        def raise_memory_error(_):
            raise MemoryError()

        patch_hash = patch('bear.hash_file', raise_memory_error)
        with patch_hash, patch('bear.ignore_append') as ignore:
            inp = [None, None]
            hash_files(inp)
            for file in inp:
                ignore.assert_called_with(file)

    @staticmethod
    def test_hash_files_filenotfound():
        """
        Test hashing a list of non-existing files.
        """
        def raise_file_not_found(_):
            raise FileNotFoundError()

        patch_hash = patch('bear.hash_file', raise_file_not_found)
        with patch_hash, patch('bear.ignore_append') as ignore:
            inp = [None, None]
            hash_files(inp)
            for file in inp:
                ignore.assert_called_with(file)

    def test_hash_files(self):
        """
        Test hashing a list of files returning hashes + paths.
        """

        file_hash = {
            'first': '123', 'second': '456',
            'original': '789', 'duplicate': '789'
        }

        def _side_effect(fname):
            return file_hash[fname]

        with patch('bear.hash_file', side_effect=_side_effect):
            inp = ['first', 'second', 'original', 'duplicate']
            out = hash_files(inp)

        expected = {}
        for key, val in file_hash.items():
            if val not in expected:
                expected[val] = [key]
            else:
                expected[val].extend([key])
        self.assertEqual(out, expected)


if __name__ == '__main__':
    main()
