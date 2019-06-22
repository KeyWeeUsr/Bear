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
        sysv = patch('sys.argv', [__name__, '--hash', target])
        hfile = patch('bear.__main__.hash_files')
        ffile_ret = [None]
        ffile = patch('bear.__main__.find_files', return_value=ffile_ret)
        fhash = patch('bear.__main__.filter_files')

        with sysv, hfile as m_hash, ffile as m_find, fhash as m_filter:
            run()
            m_find.assert_called_once_with(target)
            m_hash.assert_called_once_with(m_find.return_value)
            self.assertEqual(m_find.return_value, ffile_ret)
            m_filter.assert_called_once_with(m_hash.return_value)


if __name__ == '__main__':
    main()
