"""
Test running module in CLI.
"""

from unittest import TestCase, main
from unittest.mock import patch

from bear.__main__ import main as app_main


class MainCase(TestCase):
    def test_cli(self):
        target = 'testpath'
        with patch('bear.__main__.hash_file') as mocked:
            app_main([None, target])
            mocked.assert_called_once_with(target)


if __name__ == '__main__':
    main()
