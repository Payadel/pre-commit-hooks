import os
import tempfile
import unittest

from on_rails import (ValidationError, assert_error_detail, assert_result,
                      assert_result_with_type)

from pre_commit_hooks.run_scripts._helpers.utility import (PathType,
                                                           check_path_type,
                                                           get_file_name)


class TestUtility(unittest.TestCase):
    def test_get_file_name_give_invalid(self):
        result = get_file_name(None)
        assert_result_with_type(self, result, expected_success=False, expected_detail_type=ValidationError)
        assert_error_detail(self, result.detail, expected_title="One or more validation errors occurred",
                            expected_message="The input file path is not valid. It can not be None or empty.",
                            expected_code=400)

        result = get_file_name("")
        assert_result_with_type(self, result, expected_success=False, expected_detail_type=ValidationError)
        assert_error_detail(self, result.detail, expected_title="One or more validation errors occurred",
                            expected_message="The input file path is not valid. It can not be None or empty.",
                            expected_code=400)

        result = get_file_name("    ")
        assert_result_with_type(self, result, expected_success=False, expected_detail_type=ValidationError)
        assert_error_detail(self, result.detail, expected_title="One or more validation errors occurred",
                            expected_message="The input file path is not valid. It can not be None or empty.",
                            expected_code=400)

    def test_get_file_name_give_valid(self):
        result = get_file_name("file_name")
        assert_result(self, result, expected_success=True, expected_value="file_name")

        result = get_file_name("path1/path2/file_name")
        assert_result(self, result, expected_success=True, expected_value="file_name")

    def test_check_path_type_give_none_or_empty(self):
        self.assertRaises(ValueError, check_path_type, None)
        self.assertRaises(ValueError, check_path_type, "")
        self.assertRaises(ValueError, check_path_type, "   ")

    def test_check_path_type(self):
        with tempfile.TemporaryDirectory() as tmp_dir_name:
            file = os.path.join(tmp_dir_name, "script.sh")
            with open(file, "w") as f:
                f.write('#!/bin/bash \n\nexit 0\n')

            result = check_path_type(file)
            assert result == PathType.FILE

            result = check_path_type(tmp_dir_name)
            assert result == PathType.DIRECTORY

            result = check_path_type("invalid path")
            assert result == PathType.INVALID


if __name__ == '__main__':
    unittest.main()
