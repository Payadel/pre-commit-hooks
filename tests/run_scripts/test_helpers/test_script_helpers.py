# pragma: disable=All

import os
import tempfile
import unittest

from on_rails import (SuccessDetail, ValidationError, assert_error_detail,
                      assert_result, assert_result_detail,
                      assert_result_with_type)
from on_rails.ResultDetails.Errors import NotFoundError

from pre_commit_hooks.run_scripts._helpers.script_helpers import (
    _get_directory_scripts, _get_scripts, _run_scripts, _run_shell,
    run_scripts)
from pre_commit_hooks.run_scripts._ResultDetails.ShellError import ShellError
from pre_commit_hooks.run_scripts._ResultDetails.ShellOutput import ShellOutput


class TestRunScripts(unittest.TestCase):
    def test_get_scripts(self) -> None:
        # create a temporary directory and some files in it
        with tempfile.TemporaryDirectory() as tmp_dir_name:
            dir1 = os.path.join(tmp_dir_name, "dir1")
            os.makedirs(dir1)
            dir2 = os.path.join(tmp_dir_name, "dir2")
            os.makedirs(dir2)

            file1 = os.path.join(tmp_dir_name, "file1.py")
            with open(file1, "w") as f:
                f.write("print('file1')")
            file2 = os.path.join(dir1, "file2.py")
            with open(file2, "w") as f:
                f.write("print('file2')")
            file3 = os.path.join(dir2, "file3.py")
            with open(file3, "w") as f:
                f.write("print('file3')")

            # test with no arguments
            res = _get_scripts(None)
            assert_result(self, res, expected_success=True, expected_value=[])

            # test with files argument
            res = _get_scripts([file1])
            assert_result(self, res, expected_success=True, expected_value=[file1])

            # test with directories argument
            res = _get_scripts([dir1])
            assert_result(self, res, expected_success=True, expected_value=[file2])

            # test with both arguments
            res = _get_scripts([dir1, file1, dir2])
            res.value.sort()
            assert_result(self, res, expected_success=True, expected_value=[file2, file3, file1])

            # test with repeated files/arguments
            res = _get_scripts([file1, file2, file3, dir1, dir2, tmp_dir_name])
            res.value.sort()
            assert_result(self, res, expected_success=True, expected_value=[file2, file3, file1])

    def test_get_scripts_give_invalid_directory(self):
        res = _get_scripts([None])
        assert_result_with_type(self, res, expected_success=False, expected_detail_type=ValidationError)
        assert_error_detail(self, res.detail, expected_title="One or more validation errors occurred",
                            expected_message="None is not file or directory!", expected_code=400)

    def test_get_directory_scripts_exist_directory(self) -> None:
        # create a temporary directory and some files in it
        with tempfile.TemporaryDirectory() as tmp_dir_name:
            # Empty directory
            res = _get_directory_scripts(tmp_dir_name)
            assert_result(self, res, expected_success=True, expected_value=[])

            file1 = os.path.join(tmp_dir_name, "script1.py")
            with open(file1, "w") as f:
                f.write("print('script1')")
            file2 = os.path.join(tmp_dir_name, "script2.py")
            with open(file2, "w") as f:
                f.write("print('script2')")

            # test with files in the directory
            res = _get_directory_scripts(tmp_dir_name)
            assert_result(self, res, expected_success=True, expected_value=[file1, file2])

            # Make sure returns only files
            sub_dir = os.path.join(tmp_dir_name, "sub_dir")
            os.makedirs(sub_dir)

            res = _get_directory_scripts(tmp_dir_name)
            assert_result(self, res, expected_success=True, expected_value=[file1, file2])

    def test_get_directory_scripts_non_exist_directory(self):
        # test with a non-existing directory
        res = _get_directory_scripts("non-existing-directory")
        assert_result_with_type(self, res, expected_success=False, expected_detail_type=NotFoundError)
        assert_error_detail(self, target_error_detail=res.detail, expected_title="NotFound Error",
                            expected_message="Directory (non-existing-directory) is not exists.",
                            expected_code=404)

    def test_get_directory_scripts_give_none(self):
        res = _get_directory_scripts(None)
        assert_result_with_type(self, res, expected_success=False, expected_detail_type=ValidationError)
        assert_error_detail(self, target_error_detail=res.detail,
                            expected_title="One or more validation errors occurred",
                            expected_message="Directory parameter can not be None.",
                            expected_code=400)

    def test_run_shell_ok(self):
        result = _run_shell("echo Hello")

        assert_result_with_type(self, result, expected_success=True, expected_detail_type=ShellOutput)
        assert result.detail.output == 'Hello\n'

    def test_run_shell_exit_non_zero_code(self):
        result = _run_shell("echo Error; exit 1")

        assert_result_with_type(self, result, expected_success=False, expected_detail_type=ShellError)
        assert result.detail.code == 1
        assert result.detail.output == 'Error\n\n'

    def test_run_shell_exec_script_with_args(self):
        # create a temporary directory and script file in it
        with tempfile.TemporaryDirectory() as tmp_dir_name:
            file = os.path.join(tmp_dir_name, "script.sh")
            with open(file, "w") as f:
                f.write('#!/bin/bash \n\necho "Args: $*"\n')

            args = ['arg1', 'arg2']
            result = _run_shell(f"chmod +x {file}") \
                .on_success(lambda: _run_shell(f"{file} {' '.join(args)}"))
            print(result.detail)
            assert_result_with_type(self, result, expected_success=True, expected_detail_type=ShellOutput)
            assert result.detail.output == 'Args: arg1 arg2\n'

    def test_run_shell_give_none_or_empty(self):
        result = _run_shell(None)
        assert_result_with_type(self, result, expected_success=False, expected_detail_type=ValidationError)
        assert_error_detail(self, result.detail, expected_title="One or more validation errors occurred",
                            expected_message="The command can not be None or empty.", expected_code=400)

        result = _run_shell("")
        assert_result_with_type(self, result, expected_success=False, expected_detail_type=ValidationError)
        assert_error_detail(self, result.detail, expected_title="One or more validation errors occurred",
                            expected_message="The command can not be None or empty.", expected_code=400)

        result = _run_shell("    ")
        assert_result_with_type(self, result, expected_success=False, expected_detail_type=ValidationError)
        assert_error_detail(self, result.detail, expected_title="One or more validation errors occurred",
                            expected_message="The command can not be None or empty.", expected_code=400)

    def test_run_scripts_give_none(self):
        result = _run_scripts(None)
        print(result)
        assert_result_with_type(self, result, expected_success=True, expected_detail_type=SuccessDetail)
        assert_result_detail(self, result.detail, expected_title="Operation was successful",
                             expected_message="All scripts executed.", expected_code=200)

    def test_run_scripts(self):
        # create a temporary directory and script files in it
        with tempfile.TemporaryDirectory() as tmp_dir_name:
            file1 = os.path.join(tmp_dir_name, "script1.sh")
            with open(file1, "w") as f:
                f.write('#!/bin/bash \n\n[ "$#" -gt 2 ] && echo "Number of inputs is more than 2" && exit 1\nexit 0\n')
            file2 = os.path.join(tmp_dir_name, "script2.sh")
            with open(file2, "w") as f:
                f.write('#!/bin/bash \n\necho "Hello"\n')
            # Give permission
            for file in [file1, file2]:
                _run_shell(f"chmod +x {file}").on_fail_raise_exception()

            result = _run_scripts([file1, file2])
            assert_result_with_type(self, result, expected_success=True, expected_detail_type=SuccessDetail)
            assert_result_detail(self, result.detail, expected_title="Operation was successful",
                                 expected_message="All scripts executed.", expected_code=200)

            result = _run_scripts([file1, file2], ["input1", "input2"])
            assert_result_with_type(self, result, expected_success=True, expected_detail_type=SuccessDetail)
            assert_result_detail(self, result.detail, expected_title="Operation was successful",
                                 expected_message="All scripts executed.", expected_code=200)

            result = _run_scripts([file1, file2], ["input1", "input2", "more_than_2_parameters"])
            assert_result_with_type(self, result, expected_success=False, expected_detail_type=ShellError)
            assert_result_detail(self, result.detail, expected_title="The shell exited with code 1",
                                 expected_message=f"The ({file1} input1 input2 more_than_2_parameters) "
                                                  f"command failed with code 1. Please see output for more details.",
                                 expected_code=1)

    def test_run_scripts_give_none(self):
        result = run_scripts()
        assert_result_with_type(self, result, expected_success=True, expected_detail_type=SuccessDetail)
        assert_result_detail(self, result.detail, expected_title="Operation was successful",
                             expected_message="No script(s) found.",
                             expected_code=200)


if __name__ == '__main__':
    unittest.main()
