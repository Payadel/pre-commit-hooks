# pragma: disable=All
import subprocess
import unittest

from pre_commit_hooks.run_scripts._ResultDetails.ShellOutput import ShellOutput


class MyTestCase(unittest.TestCase):
    def test_shell_output(self):
        command = "echo 'Hello, world!'"
        output = subprocess.check_output(command, shell=True)
        shell_output = ShellOutput(output=output)
        assert shell_output.title == 'Operation was successful'
        assert shell_output.message is None
        assert shell_output.code is None
        assert shell_output.output.strip() == "Hello, world!"

        title = "My Shell Output"
        message = "Here is the output of my shell command:"
        code = 0
        shell_output = ShellOutput(output=output, title=title, message=message, code=code)
        assert shell_output.title == title
        assert shell_output.message == message
        assert shell_output.code == code
        assert shell_output.output.strip() == "Hello, world!"


if __name__ == '__main__':
    unittest.main()
