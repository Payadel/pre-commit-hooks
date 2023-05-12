import unittest
from unittest.mock import patch

from on_rails import (ErrorDetail, assert_result, assert_result_detail,
                      assert_result_with_type)

from pre_commit_hooks.document_oriented.git import (get_changed_files,
                                                    get_remote_branch_name)


class TestGetRemoteBranchName(unittest.TestCase):
    @patch('subprocess.run')
    def test_success(self, mock_subprocess_run):
        mock_subprocess_run.return_value.returncode = 0
        mock_subprocess_run.return_value.stdout = b'remote-branch\n'

        result = get_remote_branch_name()

        assert_result(self, result, expected_success=True, expected_value='remote-branch')

    @patch('subprocess.run')
    def test_no_such_branch(self, mock_subprocess_run):
        mock_subprocess_run.return_value.returncode = 128
        mock_subprocess_run.return_value.stderr = b'fatal: no such branch: master\n'

        result = get_remote_branch_name()

        assert_result(self, result, expected_success=True, expected_value=None)

    @patch('subprocess.run')
    def test_no_upstream_configured(self, mock_subprocess_run):
        mock_subprocess_run.return_value.returncode = 128
        mock_subprocess_run.return_value.stderr = b'fatal: no upstream configured for branch master\n'

        result = get_remote_branch_name()

        assert_result(self, result, expected_success=True, expected_value=None)

    @patch('subprocess.run')
    def test_unexpected_error(self, mock_subprocess_run):
        mock_subprocess_run.return_value.returncode = 128
        mock_subprocess_run.return_value.stderr = b'fatal: unexpected error!\n'

        result = get_remote_branch_name()

        assert_result_with_type(self, result, expected_success=False, expected_detail_type=ErrorDetail)
        assert_result_detail(self, result.detail, expected_title="get remote branch name failed.",
                             expected_message="fatal: unexpected error!", expected_code=128)


class TestGetChangedFiles(unittest.TestCase):
    @patch('subprocess.run')
    @patch('subprocess.check_output')
    def test_branch_has_not_upstream(self, mock_check_output, mock_run):
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = b''

        mock_check_output.return_value = b'file1\nfile2\n'

        result = get_changed_files()

        assert_result(self, result, True, expected_value=[])

    @patch('subprocess.run')
    @patch('subprocess.check_output')
    def test_ok(self, mock_check_output, mock_run):
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = b'main\n'

        mock_check_output.return_value = b'src/file.txt\nfile2.md\n'

        result = get_changed_files()

        assert_result(self, result, True, expected_value=['src/file.txt', 'file2.md'])


if __name__ == '__main__':
    unittest.main()
