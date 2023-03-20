import argparse
import os.path
from typing import List, Optional

from pre_commit_hooks.libs.Details import (ErrorDetail, SuccessDetail,
                                           ValidationErrorDetail)
from pre_commit_hooks.libs.KeyValue import KeyValue
from pre_commit_hooks.libs.Result import Result
from pre_commit_hooks.libs.Utility import Utility


def get_args():
    """ Get CLI parameters """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-d', '--directory', action='append',
        help='The path of the scripts to be executed.',
    )
    parser.add_argument(
        '-f', '--file', action='append',
        help='The path of the script file to be executed.',
    )
    return parser.parse_known_args()


def inputs_must_valid(args) -> Result:
    """ Checks CLI parameters are correct or not. """
    directories = args.directory
    files = args.file

    if not directories and not files:
        return Result.fail(ValidationErrorDetail(
            message="At least one directory or file must be set."))

    errors: List[KeyValue] = []
    if directories:
        for directory in directories:
            if not os.path.isdir(directory):
                errors.append(KeyValue(key=directory, message="Can not find directory."))

    if files:
        for file in files:
            if not os.path.isfile(file):
                errors.append(KeyValue(key=file, message="Can not find file."))

    if len(errors) > 0:
        return Result.fail(ValidationErrorDetail(errors=errors))
    return Result.ok()


def run_script(script_path: str, args: List[str]) -> Result:
    """ Execute single script """
    try:
        result = Utility.run_shell([script_path] + args)
        return result
    except Exception as error:  # pylint: disable=broad-exception-caught
        return Result.fail(ErrorDetail(title="An exception has occurred.", exception=error))


def run_scripts(files: Optional[List[str]],
                directories: Optional[List[str]],
                args: Optional[List[str]]) -> Result:
    """ Collect all scripts and execute them """
    scripts = get_scripts(files, directories)
    if len(scripts) == 0:
        return Result.ok(SuccessDetail(message="No script(s) found."))
    print(f"{len(scripts)} script(s) found.")

    for script in scripts:
        print(f"Running {Utility.get_file_name(script)}...", end="")
        result = run_script(script, args)
        if result.success:
            print("done.")
        else:
            print("failed.")
            return result
    return Result.ok()


def get_scripts(files: Optional[List[str]], directories: Optional[List[str]]) -> List[str]:
    """ Collect scripts and return paths """
    result: List[str] = []
    if files:
        result += files
    if directories:
        for directory in directories:
            result += Utility.get_sorted_scripts(directory)
    return result


def run() -> Result:
    """ Main runner """
    args, other = get_args()
    result = inputs_must_valid(args)
    if not result.success:
        return result
    return run_scripts(args.file, args.directory, other)


def main():
    """ Run program and print result """
    result = run()
    if result.detail:
        print("\n")
        print(result.detail)
    if not result.success:
        print_help()
    raise SystemExit(result.code())


def print_help() -> None:
    """ Prints helper message to user """
    print("Use --help to get more information.")


if __name__ == '__main__':
    main()
