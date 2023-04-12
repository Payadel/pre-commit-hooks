# pylint: disable=all

import unittest

from on_rails import (ValidationError, assert_error_detail,
                      assert_result_with_type)

from pre_commit_hooks.run_scripts._helpers.argument_helpers import get_args
from tests._helpers import assert_input_args, get_test_path


class TestArgumentHelpers(unittest.TestCase):
    def test_get_args_known_args_without_validation(self):
        result = get_args(validate_inputs=False, args=['-f', 'file1', '-d', 'dir1', '-f', 'file2', '-d', 'dir2'])

        assert_input_args(self, result, expected_files=['file1', 'file2'], expected_directories=['dir1', 'dir2'])

    def test_get_args_unknown_args_without_validation(self):
        result = get_args(validate_inputs=False, args=['-f', 'file', '-d', 'dir', '-a', 'aaa', 'bbb'])

        assert_input_args(self, result, expected_files=['file'], expected_directories=['dir'],
                          expected_other=['-a', 'aaa', 'bbb'])

    def test_get_args_validation_file(self):
        cwd = get_test_path()
        file_path = f"{cwd}/fake-scripts/single-script.py"
        result = get_args(validate_inputs=True, args=['-f', file_path])

        assert_input_args(self, result, expected_files=[file_path])

    def test_get_args_validation_dir(self):
        cwd = get_test_path()
        dir_path = f"{cwd}/fake-scripts/commit/"
        result = get_args(validate_inputs=True, args=['-d', dir_path])

        assert_input_args(self, result, expected_directories=[dir_path])

    def test_get_args_validation_complete(self):
        cwd = get_test_path()
        file_path = f"{cwd}/fake-scripts/single-script.py"
        dir_path = f"{cwd}/fake-scripts/commit/"

        result = get_args(validate_inputs=True, args=['-f', file_path, '-d', dir_path])

        assert_input_args(self, result, expected_directories=[dir_path], expected_files=[file_path])

    def test_get_args_validation_error(self):
        result = get_args(validate_inputs=True, args=['-f', 'file1', '-d', 'dir1', '-a', 'aaa', 'bbb'])
        assert_result_with_type(self, result, expected_success=False, expected_detail_type=ValidationError)

        assert_error_detail(self, result.detail, expected_title="One or more validation errors occurred",
                            expected_errors={'dir1': 'Can not find the directory.', 'file1': 'Can not find the file.'},
                            expected_code=400)

    def test_get_args_validation_no_file_or_directory(self):
        result = get_args(validate_inputs=True, args=['-a', 'aaa', 'bbb'])

        assert_result_with_type(self, result, expected_success=False, expected_detail_type=ValidationError)
        assert_error_detail(self, result.detail, expected_title="One or more validation errors occurred",
                            expected_message="At least one directory or file must be set.",
                            expected_code=400)


if __name__ == '__main__':
    unittest.main()
