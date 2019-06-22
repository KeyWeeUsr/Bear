"""
Test running module in CLI.
"""

from unittest import TestCase, main
from unittest.mock import patch

from bear.__main__ import run


class MainCase(TestCase):
    def test_cli(self):
        target = 'testpath'
        hash_file = patch('bear.__main__.hash_file')
        sysargv = patch('sys.argv', [__name__, target])
        with sysargv, hash_file as mocked:
            run()
            mocked.assert_called_once_with(target)


if __name__ == '__main__':
    main()
