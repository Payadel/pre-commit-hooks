import unittest
from unittest.mock import patch

from on_rails import assert_result

from pre_commit_hooks.document_oriented.git import (get_changed_files,
                                                    get_remote_branch_name)


class TestGetRemoteBranchName(unittest.TestCase):
    @patch('subprocess.check_output')
    def test_ok(self, mock_check_output):
        mock_check_output.return_value = b'main\n'

        result = get_remote_branch_name()
        assert_result(self, result, True, expected_value='main')


class TestGetChangedFiles(unittest.TestCase):
    @patch('subprocess.check_output')
    def test_branch_has_not_upstream(self, mock_check_output):
        mock_check_output.side_effect = lambda args: b'\n' if args == ["git", "rev-parse", "--abbrev-ref",
                                                                       "@{upstream}"] else b'file1\nfile2'

        result = get_changed_files()

        assert_result(self, result, True, expected_value=[])

    @patch('subprocess.check_output')
    def test_ok(self, mock_check_output):
        mock_check_output.side_effect = lambda args: b'main\n' if args == ["git", "rev-parse", "--abbrev-ref",
                                                                           "@{upstream}"] else b'src/file.txt\nfile2.md'

        result = get_changed_files()

        assert_result(self, result, True, expected_value=['src/file.txt', 'file2.md'])


if __name__ == '__main__':
    unittest.main()
