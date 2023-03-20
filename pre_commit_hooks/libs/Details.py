from typing import List, Optional

from pre_commit_hooks.libs.KeyValue import KeyValue
from pre_commit_hooks.libs.Result import Detail


class ErrorDetail(Detail):
    errors: Optional[List[KeyValue]]
    exception: Optional[Exception]

    def __init__(self, title: Optional[str] = "Error",
                 message: Optional[str] = None,
                 code: Optional[int] = 1,
                 errors: Optional[List[KeyValue]] = None,
                 exception: Optional[Exception] = None):
        super().__init__(title, message, code)
        self.errors = errors
        self.exception = exception

    def __str__(self):
        result = super().__str__()
        if self.errors:
            result += "Errors:\n"
            for error in self.errors:
                result += f"\t{error.key}: {error.message}\n"
        if self.exception:
            result += f"Exception Data:\n{self.exception}"
        return result


class ValidationErrorDetail(ErrorDetail):
    def __init__(self, title: Optional[str] = "Validation Error",
                 message: Optional[str] = "One or more fields are not valid.",
                 code: Optional[int] = 1,
                 errors: Optional[List[KeyValue]] = None):
        super().__init__(title, message, code, errors)


class RunShellErrorDetail(ErrorDetail):
    script_name: Optional[str] = None
    output: Optional[str] = None

    def __init__(self, title: Optional[str] = "Run Script failed",
                 message: Optional[str] = None, code: Optional[int] = 1,
                 script_name: Optional[str] = None, output: Optional[str] = None):
        super().__init__(title, message, code, errors=None)
        self.script_name = script_name
        self.output = output
        if message:
            self.message = message
        elif script_name:
            self.message = f"Can not execute '{script_name}'"

    def __str__(self):
        result = super().__str__()
        if self.output:
            result += f"More data:\n{self.output}"
        return result


class SuccessDetail(Detail):
    def __init__(self, title: Optional[str] = "Operation was successful",
                 message: Optional[str] = None,
                 code: Optional[int] = 0):
        super().__init__(title, message, code)
