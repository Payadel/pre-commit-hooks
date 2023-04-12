from typing import Optional

from on_rails import SuccessDetail


class ShellOutput(SuccessDetail):
    """
    The ShellOutput class represents the output of a shell command, including a title, message, code,
    and the actual output as a string.
    """
    output: str = ""

    def __init__(self, output: bytes,
                 title: Optional[str] = None,
                 message: Optional[str] = None,
                 code: Optional[int] = None):
        super().__init__(title=title, message=message, code=code)
        self.output = output.decode('utf-8') if output else ""

    def __str__(self):
        result = super().__str__()
        result += f"Output: \n{self.output}\n"
        return result
