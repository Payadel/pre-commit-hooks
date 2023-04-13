# pylint: disable=all
import os
import tempfile
import unittest

from on_rails import (ValidationError, assert_error_detail,
                      assert_result_with_type)

from pre_commit_hooks.run_scripts._helpers.argument_helpers import get_args
from tests._helpers import assert_input_args


class TestArgumentHelpers(unittest.TestCase):
    def test_get_args_known_args_without_validation(self):
        result = get_args(validate_inputs=False, args=['-f', 'file1', '-d', 'dir1', '-f', 'file2', '-d', 'dir2'])

        assert_input_args(self, result, expected_files=['file1', 'file2'], expected_directories=['dir1', 'dir2'])

    def test_get_args_unknown_args_without_validation(self):
        result = get_args(validate_inputs=False, args=['-f', 'file', '-d', 'dir', '-a', 'aaa', 'bbb'])

        assert_input_args(self, result, expected_files=['file'], expected_directories=['dir'],
                          expected_other=['-a', 'aaa', 'bbb'])

    def test_get_args_validation_file(self):
        # create a temporary directory and some files in it
        with tempfile.TemporaryDirectory() as tmp_dir_name:
            file = os.path.join(tmp_dir_name, "file.py")
            with open(file, "w") as f:
                f.write("print('file1')")

            result = get_args(validate_inputs=True, args=['-f', file])

            assert_input_args(self, result, expected_files=[file])

    def test_get_args_validation_dir(self):
        # create a temporary directory and some files in it
        with tempfile.TemporaryDirectory() as tmp_dir_name:
            dir1 = os.path.join(tmp_dir_name, "dir")
            os.makedirs(dir1)

            file = os.path.join(dir1, "file.py")
            with open(file, "w") as f:
                f.write("print('file')")

            result = get_args(validate_inputs=True, args=['-d', dir1])

            assert_input_args(self, result, expected_directories=[dir1])

    def test_get_args_validation_complete(self):
        # create a temporary directory and some files in it
        with tempfile.TemporaryDirectory() as tmp_dir_name:
            dir1 = os.path.join(tmp_dir_name, "dir")
            os.makedirs(dir1)

            file1 = os.path.join(tmp_dir_name, "file1.py")
            with open(file1, "w") as f:
                f.write("print('file1')")
            file2 = os.path.join(dir1, "file2.py")
            with open(file2, "w") as f:
                f.write("print('file2')")

            result = get_args(validate_inputs=True, args=['-f', file1, '-d', dir1])

            assert_input_args(self, result, expected_directories=[dir1], expected_files=[file1])

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
