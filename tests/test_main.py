import os
import tempfile
import unittest

from on_rails import (SuccessDetail, ValidationError, assert_error_detail,
                      assert_result_with_type)

from pre_commit_hooks.run_scripts._helpers.script_helpers import (_get_scripts,
                                                                  _run_shell)
from pre_commit_hooks.run_scripts._ResultDetails.ShellError import ShellError
from pre_commit_hooks.run_scripts.main import main
from tests._helpers import assert_shell_error


class TestMain(unittest.TestCase):
    def test_main(self):
        with tempfile.TemporaryDirectory() as tmp_dir_name:
            dir1 = os.path.join(tmp_dir_name, "dir1")
            os.makedirs(dir1)
            dir2 = os.path.join(tmp_dir_name, "dir2")
            os.makedirs(dir2)

            file1 = os.path.join(tmp_dir_name, "file1.py")
            with open(file1, "w") as f:
                f.write('#!/bin/bash \n\n[ "$#" -gt 3 ] && echo "Number of inputs is more than 3" && exit 1\nexit 0\n')
            file2 = os.path.join(dir1, "file2.py")
            with open(file2, "w") as f:
                f.write('#!/bin/bash \n\n[ "$#" -gt 2 ] && echo "Number of inputs is more than 2" && exit 1\nexit 0\n')
            file3 = os.path.join(dir2, "file3.py")
            with open(file3, "w") as f:
                f.write('#!/bin/bash \n\n[ "$#" -gt 1 ] && echo "Number of inputs is more than 1" && exit 1\nexit 0\n')
            # Give permission
            _get_scripts([file1, dir1, dir2]) \
                .on_success(
                lambda scripts: [_run_shell(f"chmod +x {file}").on_fail_raise_exception() for file in scripts]) \
                .on_fail_raise_exception()

            # result = main(f" ")
            # assert_result_with_type(self, result, expected_success=False, expected_detail_type=ValidationError)
            # assert_error_detail(self, result.detail, expected_title="One or more validation errors occurred",
            #                     expected_message='At least one directory or file must be set.', expected_code=400)
            #
            # result = main(f"-f {file1} -d {dir1} -d {dir2} -f {file3} -d {tmp_dir_name}".split(' '))
            # assert_result_with_type(self, result, expected_success=True, expected_detail_type=SuccessDetail)
            #
            # result = main(f"   -f {file1} -d {dir1} -d {dir2} -f {file3} arg1   ".split(' '))
            # assert_result_with_type(self, result, expected_success=True, expected_detail_type=SuccessDetail)

            result = main(f"-f {file1} -d {dir1} -d {dir2} -f {file3} arg1 arg2".split(' '))
            assert_result_with_type(self, result, expected_success=False, expected_detail_type=ShellError)
            assert_shell_error(self, target_shell_error=result.detail, expected_code=1,
                               expected_command=f"{file3} arg1 arg2",
                               expected_stdout="Number of inputs is more than 1\n",
                               expected_stderr=None,
                               expected_output='Number of inputs is more than 1\n\n')

            result = main(f"-f {file1} -d {dir1} -d {dir2} -f {file3} arg1 arg2 arg3".split(' '))
            assert_result_with_type(self, result, expected_success=False, expected_detail_type=ShellError)
            assert_shell_error(self, target_shell_error=result.detail, expected_code=1,
                               expected_command=f"{file2} arg1 arg2 arg3",
                               expected_stdout="Number of inputs is more than 2\n",
                               expected_stderr=None,
                               expected_output='Number of inputs is more than 2\n\n')


if __name__ == '__main__':
    unittest.main()
