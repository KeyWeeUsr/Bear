"""
Test file and folder manipulation.
"""

from unittest import TestCase, main
from unittest.mock import patch, MagicMock, call
from os.path import join, basename

from bear import (
    find_files, filter_files, hash_files, ignore_append, find_duplicates,
    output_duplicates
)


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

    def test_find_duplicates_jobs(self):
        """
        Test finding duplicates using correct job count from parameter.
        """
        max_cpu = 666
        patch_cpu = patch('bear.cpu_count', return_value=max_cpu)
        patch_pool = patch('bear.Pool')
        with patch_cpu, patch_pool as pool:
            self.assertEqual(find_duplicates([], processes=1), {})
            self.assertEqual(find_duplicates([], processes=0), {})
            self.assertEqual(find_duplicates([], processes=4), {})

            self.assertEqual([
                # remove __iter__() calls because those return a tuple
                # iterator instead of call().__enter__().map().__iter__()
                item for item in pool.mock_calls if '__iter__' not in str(item)
            ], [
                call(processes=1),
                call().__enter__(),
                call().__enter__().map(hash_files, []),
                call().__exit__(None, None, None),

                call(processes=666),
                call().__enter__(),
                call().__enter__().map(hash_files, []),
                call().__exit__(None, None, None),

                call(processes=4),
                call().__enter__(),
                call().__enter__().map(hash_files, []),
                call().__exit__(None, None, None),
            ])

    def test_find_duplicates_chunks(self):
        """
        Test chunking list of files for multiple processes.
        """
        patch_pool = patch('bear.Pool')

        files = [str(num) for num in range(15)]

        def side_effect(folder):
            return {
                'a': files[:5],
                'b': files[5:10],
                'c': files[10:]
            }[basename(folder)]

        patch_find_files = patch('bear.find_files', side_effect=side_effect)

        # pylint: disable=confusing-with-statement
        with patch_pool as pool, patch_find_files:
            self.assertEqual(find_duplicates(['a', 'b', 'c'], processes=1), {})
            self.assertEqual(find_duplicates(['a', 'b', 'c'], processes=3), {})
            self.assertEqual(find_duplicates(['a', 'b', 'c'], processes=4), {})

            self.assertEqual([
                # remove __iter__() calls because those return a tuple
                # iterator instead of call().__enter__().map().__iter__()
                item for item in pool.mock_calls if '__iter__' not in str(item)
            ], [
                call(processes=1),
                call().__enter__(),
                # all files to single process
                call().__enter__().map(hash_files, [files]),
                call().__exit__(None, None, None),

                call(processes=3),
                call().__enter__(),
                # files chunked len / processors -> 15 // 3 chunks
                call().__enter__().map(hash_files, [
                    files[0:5], files[5:10], files[10:15]
                ]),
                call().__exit__(None, None, None),

                call(processes=4),
                call().__enter__(),
                # files chunked len / processors -> 15 // 4 chunks
                call().__enter__().map(hash_files, [
                    files[0:3], files[3:6], files[6:9], files[9:12], files[12:]
                ]),
                call().__exit__(None, None, None),
            ])

    def test_find_duplicates_join(self):
        """
        Test joining duplicates from multiple jobs.
        """
        mock_pool = MagicMock(**{
            '__enter__.return_value.map.return_value': [
                {'123': ['original'], '456': ['ori', 'dupli']},
                {'123': ['duplicate']},
                {'789': ['original'], '012': ['orig', 'dup']}
            ]
        })
        patch_pool = patch('bear.Pool', return_value=mock_pool)
        with patch_pool:
            # 789 is single-file original, ignored in filter_files()
            self.assertEqual(find_duplicates([], processes=2), {
                '012': ['orig', 'dup'],
                '123': ['original', 'duplicate'],
                '456': ['ori', 'dupli']
            })

    @staticmethod
    def test_find_duplicates_output():
        """
        Test outputing duplicates to file.
        """
        hashes = {
            '012': ['orig', 'dup'],
            b'123': ['original', 'duplicate'],
            '456': ['ori', 'dupli']
        }

        file_obj = MagicMock()
        mocked_open_inst = MagicMock(
            __enter__=MagicMock(return_value=file_obj)
        )
        patch_open = patch(
            'builtins.open', return_value=mocked_open_inst
        )
        now = '12345'
        patch_now = patch('bear.datetime', now=MagicMock(return_value=now))

        def assert_write_hashes(mock_obj):
            calls = []
            for key, value in hashes.items():
                calls += [
                    call(
                        key.encode('utf-8')
                        if not isinstance(key, bytes) else key
                    ), call(b'\n')
                ]
                calls += [
                    call(b'\t' + val.encode('utf-8') + b'\n')
                    for val in value
                ]
                calls += [call(b'\n\n')]
            mock_obj.assert_has_calls(calls)

        with patch_now, patch_open as mocked_open:
            output_duplicates(hashes)
            mocked_open.assert_called_once_with(f'{now}_duplicates.txt', 'wb')
            assert_write_hashes(file_obj.write)

        with patch_now, patch_open as mocked_open:
            out = 'custom.txt'
            output_duplicates(hashes, out=out)
            mocked_open.assert_called_once_with(out, 'wb')
            assert_write_hashes(file_obj.write)


if __name__ == '__main__':
    main()
