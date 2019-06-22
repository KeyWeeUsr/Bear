"""
Test running module in CLI.
"""

from unittest import TestCase, main
from unittest.mock import patch

from bear.__main__ import run


class MainCase(TestCase):
    def test_hash_file(self):
        target = 'testpath'
        hash_file = patch('bear.__main__.hash_file')
        sysargv = patch('sys.argv', [__name__, '--files', target])
        with sysargv, hash_file as mocked:
            run()
            mocked.assert_called_once_with(target)

    def test_find_files(self):
        target = 'testpath'
        find_file = patch('bear.__main__.find_files')
        sysargv = patch('sys.argv', [__name__, '--traverse', target])
        with sysargv, find_file as mocked:
            run()
            mocked.assert_called_once_with(target)

    def test_hash_folder(self):
        target = 'testpath'
        hash_file = patch('bear.__main__.hash_files')
        find_file = patch('bear.__main__.find_files')
        sysargv = patch('sys.argv', [__name__, '--hash', target])
        with sysargv, hash_file as mocked_hash, find_file as mocked_find:
            run()
            mocked_find.assert_called_once_with(target)
            mocked_hash.assert_called_once_with(mocked_find.return_value)


if __name__ == '__main__':
    main()
