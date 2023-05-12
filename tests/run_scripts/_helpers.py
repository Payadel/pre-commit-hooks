# pragma: disable=All

import unittest
from typing import List, Optional

from on_rails import Result

from pre_commit_hooks.run_scripts._ResultDetails.ShellError import ShellError


def assert_input_args(test_class: unittest.TestCase, target_result: Result,
                      expected_files: List[str] = None, expected_directories: List[str] = None,
                      expected_other: List[str] = []):
    test_class.assertTrue(target_result.success, msg="success")
    test_class.assertEqual(2, len(target_result.value), msg="value length")
    args, other = target_result.value

    test_class.assertEqual(expected_files, args.file, msg="files")
    test_class.assertEqual(expected_directories, args.directory, msg="directories")
    test_class.assertEqual(expected_other, other, msg="Other Arguments")


def assert_shell_error(test_class: unittest.TestCase, target_shell_error: ShellError, expected_code: int,
                       expected_command: str, expected_output: str, expected_stderr: Optional[str],
                       expected_stdout: Optional[str], expected_title: Optional[str] = None,
                       expected_message: Optional[str] = None):
    expected_title = expected_title if expected_title else f"The shell exited with code {expected_code}"
    expected_message = expected_message if expected_message else f"The ({expected_command}) command failed with " \
                                                                 f"code {expected_code}. Please see output for more details."

    test_class.assertEqual(expected_code, target_shell_error.code)
    test_class.assertEqual(expected_title, target_shell_error.title)
    test_class.assertEqual(expected_message, target_shell_error.message)
    test_class.assertEqual(expected_command, target_shell_error.command)
    test_class.assertEqual(expected_output, target_shell_error.output)
    test_class.assertEqual(expected_stderr, target_shell_error.stderr)
    test_class.assertEqual(expected_stdout, target_shell_error.stdout)
    test_class.assertTrue(f"Command: {expected_command}\nOutput: \n{expected_output}\n", str(target_shell_error))
