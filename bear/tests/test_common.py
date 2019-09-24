"""
Text functions and objects from bear.common.
"""

from unittest import TestCase, main
from unittest.mock import patch, MagicMock, call

from datetime import datetime


class CommonCase(TestCase):
    """
    TestCase for common functions and objects.
    """

    def test_oversized_file(self):
        """
        Test whether a file is within a limit.
        """
        from bear.common import oversized_file

        file = "!!" * 10000  # kind of lazy to do "random"
        limit = 1  # 1 byte limit, mock will be 2 bytes

        isfile_patch = patch("bear.common.isfile")
        stat_patch = patch("bear.common.stat", return_value=MagicMock(
            **{"st_size": limit + 1}
        ))

        with isfile_patch as mock_isfile, stat_patch as mock_stat:
            self.assertTrue(oversized_file(path=file, limit=1))
            mock_isfile.assert_called_once_with(file)
            mock_stat.assert_called_once_with(file)

    def test_oversized_file_not(self):
        """
        Test whether a file is within a limit.
        """
        from bear.common import oversized_file

        file = "!!" * 10000  # kind of lazy to do "random"
        limit = 1  # 1 byte limit, mock will be 2 bytes

        isfile_patch = patch("bear.common.isfile")
        stat_patch = patch("bear.common.stat", return_value=MagicMock(
            **{"st_size": limit - 1}
        ))

        with isfile_patch as mock_isfile, stat_patch as mock_stat:
            self.assertFalse(oversized_file(path=file, limit=1))
            mock_isfile.assert_called_once_with(file)
            mock_stat.assert_called_once_with(file)

    def test_pattern_exclude(self):
        """
        Test excluding a value with patterns included in that value.
        """
        from bear.common import pattern_exclude
        self.assertFalse(pattern_exclude("test", patterns=["a", "b", "c"]))
        self.assertTrue(pattern_exclude("test", patterns=["a", "b", "st"]))
        self.assertTrue(pattern_exclude("test", patterns=["a", "te", "st"]))

    def test_regex_exclude(self):
        """
        Test excluding a value with regex matches of that value.
        """
        from bear.common import regex_exclude
        self.assertTrue(regex_exclude(
            "/some/fol der/test", regexes=["^/some", ".*"]
        ))
        self.assertTrue(regex_exclude(
            "/some/fol der/test", regexes=[".*/test", "test"]
        ))
        self.assertFalse(regex_exclude(
            "/some/fol der/test", regexes=["nottest", "no.*match"]
        ))

    def test_remove_except_oldest(self):
        """
        Test removing all files except the oldest one.
        """
        from bear.common import remove_except_oldest as reo
        data = ["aaa", "bbb", "ccc"]

        # pylint: disable=missing-docstring,too-few-public-methods
        class Stat:
            modified = {
                "aaa": datetime(2019, 1, 1, 12, 0),
                "bbb": datetime(2019, 1, 1, 12, 1),
                "ccc": datetime(2019, 1, 1, 12, 2)
            }

            def __init__(self, path):
                self.st_mtime = self.modified[path]

        remove_patch = patch("bear.common.remove")
        stat_patch = patch("bear.common.stat", new=Stat)
        with stat_patch, remove_patch as mock_remove:
            reo(data)
        self.assertEqual(
            mock_remove.call_args_list, [call(item) for item in data][1:]
        )

    def test_remove_except_newest(self):
        """
        Test removing all files except the oldest one.
        """
        from bear.common import remove_except_newest as ren
        data = ["aaa", "bbb", "ccc"]

        # pylint: disable=missing-docstring,too-few-public-methods
        class Stat:
            modified = {
                "aaa": datetime(2019, 1, 1, 12, 0),
                "bbb": datetime(2019, 1, 1, 12, 1),
                "ccc": datetime(2019, 1, 1, 12, 2)
            }

            def __init__(self, path):
                self.st_mtime = self.modified[path]

        remove_patch = patch("bear.common.remove")
        stat_patch = patch("bear.common.stat", new=Stat)
        with stat_patch, remove_patch as mock_remove:
            ren(data)
        self.assertEqual(
            mock_remove.call_args_list,
            # reverse + slice
            [call(item) for item in data][::-1][1:]
        )


if __name__ == '__main__':
    main()
