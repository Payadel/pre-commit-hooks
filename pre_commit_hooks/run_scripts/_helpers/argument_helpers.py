import argparse
import os
from typing import Dict, Optional, Sequence

from on_rails import Result, def_result
from on_rails.ResultDetails.Errors import ValidationError


@def_result()
def get_args(validate_inputs: bool = True,
             args: Optional[Sequence[str]] = None) -> Result[argparse.ArgumentParser]:
    """
    This function returns an instance of argparse.ArgumentParser and validates the inputs if specified.

    :param validate_inputs: A boolean flag indicating whether or not to validate the inputs, defaults to True
    :type validate_inputs: bool (optional)
    :param args: args is an optional parameter of type Sequence[str], which represents the command-line arguments passed to
    the program. If this parameter is not provided, the program will use the arguments passed to it when it was executed
    :type args: Optional[Sequence[str]]
    :return: The function `get_args` returns a `Result` object that contains an instance of `argparse.ArgumentParser`. The
    `Result` object is obtained by calling the `_get_args` function and then applying an operation to validate the inputs if
    the `validate_inputs` parameter is set to `True`.
    """
    return _get_args(args) \
        .on_success_operate_when(validate_inputs,
                                 lambda value: _inputs_must_valid(value[0]).on_success(lambda: value)
                                 )


@def_result()
def _get_args(args: Optional[Sequence[str]] = None) -> Result[argparse.ArgumentParser]:
    """
    The function defines a command line argument parser that accepts directory and file paths as inputs and returns a
    `Result` object containing the parsed command-line arguments obtained from the `argparse` module.
    """

    return _get_parser() \
        .on_success(lambda parser: parser.parse_known_args(args))


@def_result()
def _get_parser() -> Result[argparse.ArgumentParser]:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-d', '--directory', action='append',
        help='The path of the scripts to be executed.',
    )
    parser.add_argument(
        '-f', '--file', action='append',
        help='The path of the script file to be executed.',
    )
    parser.parse_known_args()
    return Result.ok(parser)


@def_result()
def _inputs_must_valid(args) -> Result:
    """
    The function checks if the input directories and files are valid and returns a result indicating success or failure.

    :param args: The `args` parameter contains the command line arguments passed to a
    Python script or function. It is used to extract the `directory` and `file` arguments, which are expected to be
    lists of strings representing directories and files, respectively.

    :return: Returns a `Result` object. If there are no errors, it returns a
    successful `Result` object with no errors. If there are errors, it returns a failed `Result` object with a
    `ValidationError` object containing the errors.
    """
    directories = args.directory
    files = args.file

    if not directories and not files:
        return Result.fail(ValidationError(message="At least one directory or file must be set."))

    errors: Dict[str, str] = {}
    if directories:
        for directory in directories:
            if not os.path.isdir(directory):
                errors[directory] = "Can not find the directory."

    if files:
        for file in files:
            if not os.path.isfile(file):
                errors[file] = "Can not find the file."

    if len(errors) > 0:
        return Result.fail(ValidationError(errors=errors))
    return Result.ok()
