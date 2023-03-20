from typing import Any, Optional


class Detail:
    title: Optional[str]
    message: Optional[str]
    code: Optional[int]

    def __init__(self, title: Optional[str] = None,
                 message: Optional[str] = None,
                 code: Optional[int] = None):
        self.title = title
        self.message = message
        self.code = code

    def __str__(self):
        result: str = ""

        if self.title:
            result += f"Title: {self.title}\n"
        if self.message:
            result += f"Message: {self.message}\n"
        if self.code:
            result += f"Code: {self.code}\n"

        return result


class Result:
    success: bool
    detail: Optional[Detail] = None
    value: Optional[Any] = None

    def __init__(self, success: bool, detail: Optional[Detail]):
        self.success = success
        self.detail = detail

    @staticmethod
    def ok(detail: Optional[Detail] = None):
        return Result(True, detail)

    @staticmethod
    def fail(detail: Optional[Detail] = None):
        return Result(False, detail)

    def code(self):
        if self.detail and self.detail.code:
            return self.detail.code
        if self.success:
            return 0
        return 1
