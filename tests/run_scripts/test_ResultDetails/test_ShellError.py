# pragma: disable=All

import subprocess
import unittest

from pre_commit_hooks.run_scripts._ResultDetails.ShellError import ShellError
from tests.run_scripts._helpers import assert_shell_error


class TestShellError(unittest.TestCase):
    def test_shell_error(self):
        command = "ls /nonexistent_directory"
        try:
            subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as exc:
            error = ShellError(command=command, exit_code=exc.returncode, stdout=exc.output, stderr=exc.stderr)
            assert_shell_error(self, target_shell_error=error, expected_code=2, expected_command=command,
                               expected_stdout="ls: cannot access \'/nonexistent_directory\': No such file or directory\n",
                               expected_stderr=None,
                               expected_output='ls: cannot access \'/nonexistent_directory\': No such file or directory\n\n')


if __name__ == '__main__':
    unittest.main()
