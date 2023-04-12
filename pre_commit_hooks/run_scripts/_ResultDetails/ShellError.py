from typing import Any, List, Optional

from on_rails import ErrorDetail


class ShellError(ErrorDetail):
    """
    This is a Python class that stores the output of a shell command when it failed,
    including the command itself, exit code, stdout, and stderr.

    :param command: The shell command that was executed and resulted in this object
    :type command: str

    :param exit_code: The exit code of the shell command
    :type exit_code: int

    :param stdout: The standard output of the executed command, represented as bytes
    :type stdout: bytes

    :param stderr: The standard error of the executed command, represented as bytes
    :type stderr: bytes

    :param title: The title of the error message that will be displayed
    :type title: Optional[str]

    :param message: The message to be displayed when the command fails, indicating the command that failed and the exit
    code
    :type message: Optional[str]

    :param more_data: `more_data` is an optional parameter that can be used to pass additional data to the `ShellError`
    object. It is a list of any type of data that may be relevant to the error. This can be useful for providing
    additional context or information about the error
    :type more_data: Optional[List[Any]]
    """

    command: str
    output: str
    stdout: Optional[str]
    stderr: Optional[str]

    def __init__(self, command: str,
                 exit_code: int,
                 stdout: bytes,
                 stderr: bytes,
                 title: Optional[str] = None,
                 message: Optional[str] = None,
                 more_data: Optional[List[Any]] = None):
        super().__init__(code=exit_code, more_data=more_data)
        self.title = title if title else f"The shell exited with code {exit_code}"
        self.message = message if message else f"The ({command}) command failed with code {exit_code}. " \
                                               f"Please see output for more details."
        self.command = command
        self.stdout = stdout.decode('utf-8') if stdout else None
        self.stderr = stderr.decode('utf-8') if stderr else None
        self.output = f"{self.stdout}\n" if self.stdout else "" \
                                                             + self.stderr if self.stderr else ""

    def __str__(self):
        result = super().__str__()
        result += f"Command: {self.command}\n"
        result += f"Output: \n{self.output}\n"
        return result
