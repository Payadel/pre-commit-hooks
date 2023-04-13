import os
from enum import Enum

from on_rails import Result, ValidationError, def_result


@def_result()
def get_file_name(file_path: str) -> Result[str]:
    """ Get file name base file path """
    if file_path is None or file_path.strip() == '':
        return Result.fail(ValidationError(
            message="The input file path is not valid. It can not be None or empty."))
    return Result.ok(os.path.basename(file_path))


class PathType(Enum):
    """
    The class defines an enumeration of three path types: file, directory, and invalid.
    """
    FILE = 1
    DIRECTORY = 2
    INVALID = 3


def check_path_type(path: str):
    """
    The function checks the type of a given path and returns whether it is a file, directory, or invalid.

    :param path: The `path` parameter is a string that represents a file or directory path
    :type path: str
    """

    if path is None or path.strip() == '':
        raise ValueError("Path can not be None or empty.")

    if os.path.isfile(path):
        return PathType.FILE
    if os.path.isdir(path):
        return PathType.DIRECTORY
    return PathType.INVALID
