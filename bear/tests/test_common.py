"""
Text functions and objects from bear.common.
"""

from unittest import TestCase, main
from unittest.mock import patch, MagicMock


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


if __name__ == '__main__':
    main()
