"""
Test running module in CLI.
"""

from unittest import TestCase, main
from unittest.mock import patch, call, MagicMock
from argparse import Namespace

from bear.common import Hasher
from bear.context import Context
from bear.__main__ import run, set_log_levels


class MainCase(TestCase):
    """
    Testing CLI parameters and __main__.py.
    """

    def test_print_logo(self):
        """
        Test (not) printing logo according to different CLI options.
        """
        from bear import LOGO_HELP, LOGO
        from bear.__main__ import print_logo

        with patch("bear.__main__.print") as mock_print:
            print_logo(Context(Namespace(quiet=True)))
            print_logo(Context(Namespace(version=True)))
            mock_print.assert_not_called()

        with patch("bear.__main__.print") as mock_print:
            print_logo(Context(Namespace(quiet=False)))
            print_logo(Context(Namespace(version=False)))
            self.assertEqual(
                mock_print.call_args_list,
                [call(LOGO), call(LOGO)]
            )

        sysargv = patch('sys.argv', [__name__])
        with sysargv, patch("bear.__main__.print") as mock_print:
            print_logo(Context(Namespace(quiet=False)))
            print_logo(Context(Namespace(version=False)))
            self.assertEqual(
                mock_print.call_args_list,
                [call(LOGO_HELP), call(LOGO_HELP)]
            )

    def test_global_log_level(self):
        """
        Test setting log level for all Bear loggers.
        """
        mock_logger = MagicMock()
        patch_get = patch(
            'bear.__main__.logging.getLogger',
            return_value=mock_logger
        )
        with patch_get as get:
            set_log_levels(9000)
            self.assertEqual(get.mock_calls, [
                call('bear.hashing'), call('bear'),
                call('bear.output'), call('bear.__main__')
            ])
            self.assertEqual(mock_logger.mock_calls, [call.setLevel(9000)] * 4)

    @staticmethod
    def test_hash_file():
        """
        Test calling hashing function for a file.
        """
        target = 'testpath'
        hash_file = patch('bear.__main__.hash_file')
        sysargv = patch('sys.argv', [__name__, '--files', target])
        with sysargv, hash_file as mocked:
            run()
            mocked.assert_called_once_with(path=target, hasher=Hasher.MD5)

    @staticmethod
    def test_find_files():
        """
        Test calling function for collecting all files in a folder.
        """
        target = 'testpath'
        context = Context(Namespace(
            traverse=[target], files=[], hash=[], duplicates=[]
        ))
        ctx = patch("bear.__main__.Context", return_value=context)
        find_file = patch('bear.__main__.find_files')
        sysargv = patch('sys.argv', [__name__, '--traverse', target])
        with sysargv, ctx, find_file as mocked:
            run()
            mocked.assert_called_once_with(ctx=context, folder=target)

    def test_hash_folder(self):
        """
        Test collecting all files in a folder and calling hashing
        function on them.
        """
        target = 'testpath'
        context = Context(Namespace(
            hash=[target], traverse=[], files=[], duplicates=[]
        ))
        ctx = patch("bear.__main__.Context", return_value=context)
        sysv = patch('sys.argv', [__name__, '--hash', target])
        hfile = patch('bear.__main__.hash_files')
        ffile_ret = [None]
        ffile = patch('bear.__main__.find_files', return_value=ffile_ret)
        fhash = patch('bear.__main__.filter_files')

        with sysv, ctx, hfile as m_hash, ffile as m_find, fhash as m_filter:
            run()
            m_find.assert_called_once_with(ctx=context, folder=target)
            m_hash.assert_called_once_with(
                files=m_find.return_value, hasher=Hasher.MD5
            )
            self.assertEqual(m_find.return_value, ffile_ret)
            m_filter.assert_called_once_with(m_hash.return_value)


if __name__ == '__main__':
    main()
