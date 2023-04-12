import os
import subprocess
from typing import List, Optional

from on_rails import Result, SuccessDetail, ValidationError, def_result
from on_rails.ResultDetails.Errors import NotFoundError

from pre_commit_hooks.run_scripts._helpers.utility import (PathType,
                                                           check_path_type,
                                                           get_file_name)
from pre_commit_hooks.run_scripts._ResultDetails.ShellError import ShellError
from pre_commit_hooks.run_scripts._ResultDetails.ShellOutput import ShellOutput


@def_result()
def run_scripts(files: Optional[List[str]] = None,
                directories: Optional[List[str]] = None,
                args: Optional[List[str]] = None) -> Result:
    """
    The function runs a list of scripts with optional arguments.

    :param files: A list of file paths to individual scripts that need to be run
    :type files: Optional[List[str]]

    :param directories: The `directories` parameter is a list of strings that contains the paths of directories
    where the scripts are located. If this parameter is not provided, it defaults to an empty list
    :type directories: Optional[List[str]]

    :param args: The `args` parameter is an optional list of strings that represents the command line arguments
    to be passed to the scripts being run. These arguments can be used to modify the behavior of the scripts or
    provide additional input to them.
    :type args: Optional[List[str]]
    """

    files = files or []
    directories = directories or []

    return _get_scripts(files + directories) \
        .on_success_operate_when(lambda scripts: len(scripts) == 0,
                                 lambda: Result.ok(detail=SuccessDetail(message="No script(s) found.")),
                                 break_rails=True) \
        .on_success_tee(lambda scripts: print(f"{len(scripts)} script(s) found.")) \
        .on_success(lambda scripts: _run_scripts(scripts, args))


@def_result()
def _get_scripts(files_or_directories: Optional[List[str]]) -> Result[List[str]]:
    """
    This function takes a list of file or directory paths, Collect files, and returns a list of unique file
    paths.

    :param files_or_directories: The parameter `files_or_directories` is a list of strings that represents either
    file paths or directory paths.
    :type files_or_directories: Optional[List[str]]

    :return: a `Result` object that contains either a list of strings representing file paths
    """

    files_or_directories = files_or_directories or []
    result_scripts = set()
    for file_or_dir in files_or_directories:
        if file_or_dir is None:
            return Result.fail(ValidationError(message="None is not file or directory!"))

        path_type = check_path_type(file_or_dir)
        if path_type == PathType.FILE:
            result_scripts.add(file_or_dir)
        elif path_type == PathType.DIRECTORY:
            result = _get_directory_scripts(file_or_dir) \
                .on_success_tee(lambda scripts: result_scripts.update(scripts))
            if not result.success:  # pragma: no cover
                return result
        else:
            return Result.fail(ValidationError(
                message=f"Seems {file_or_dir} is not a file or directory! "
                        f"Only files and directories are allowed."))  # pragma: no cover
    unique_list = list(result_scripts)
    return Result.ok(unique_list)  # Make list unique


@def_result()
def _get_directory_scripts(directory: str) -> Result[List[str]]:
    """
    This function takes a directory path as input, retrieves a list of scripts in that directory, sorts them alphabetically,
    and returns the sorted list.

    :param directory: A string representing the directory path where the scripts are located
    :type directory: str

    :return: a `Result` object that contains a list of sorted script file paths. The `Result` object is a custom class that
    likely includes information about whether the operation was successful or not, and any associated error messages.
    """

    if directory is None:
        return Result.fail(ValidationError(message="Directory parameter can not be None."))
    if not os.path.isdir(directory):
        return Result.fail(NotFoundError(message=f"Directory ({directory}) is not exists."))

    scripts = os.listdir(directory)  # Get all files and directories
    scripts = [os.path.join(directory, script) for script in scripts]  # Get full path
    scripts = [script for script in scripts if check_path_type(script) is PathType.FILE]  # Filter only files
    scripts.sort()

    return Result.ok(scripts)


@def_result()
def _run_scripts(files: Optional[List[str]], args: Optional[List[str]] = None) -> Result:
    """
    This function runs a list of scripts with optional arguments and returns a result indicating success or failure.

    :param files: A list of file names (strings) representing the scripts to be executed
    :type files: Optional[List[str]]

    :param args: args is an optional list of strings that represents the command line arguments to be passed to
    the scripts.
    :type args: Optional[List[str]]

    :return: a `Result` object. If all scripts are executed successfully, the `Result` object will have a success detail
    message "All scripts executed." If any script fails, the `Result` object will have a failure detail message.
    """

    files = files or []
    args_str = ' '.join(args) if args else ''

    for file in files:
        get_file_name(file) \
            .on_success_tee(lambda name: print(f"Running {name}...", end="")) \
            .on_fail_tee(lambda prev_result: (
            print(f"Warning: Can not detect script name ({file})."),
            print("Running...")
        ))
        command = f"{file} {args_str}"
        result = _run_shell(command) \
            .on_success_tee(lambda: print("done.")) \
            .on_fail_tee(lambda: print("failed."))
        if not result.success:
            return result

    return Result.ok(detail=SuccessDetail(message="All scripts executed."))


@def_result()
def _run_shell(command: str) -> Result:
    """
    This function runs a shell command and returns a result object indicating success or failure along with any
    relevant output or error information.

    :param command: The command to be executed in the shell. It should be a string containing the command and any arguments
    or options. For example, "ls -l" or "git commit -m 'Initial commit'"
    :type command: str

    :return: The function returns a `Result` object. If the `process` executed successfully (i.e., `returncode`
    is 0), it returns a `Result` object with `ok` status and a `ShellOutput` object containing the output of the shell
    command. If the `process` failed to execute (i.e., `returncode` is not 0),it returns a `Result` object with
    `fail` status and a `ShellError` object containing the error information.
    """

    if not command or command is None or command.strip() == "":
        return Result.fail(ValidationError(message="The command can not be None or empty."))

    process = subprocess.run(command, stderr=subprocess.PIPE, stdout=subprocess.PIPE, check=False, shell=True)

    if process.returncode == 0:
        return Result.ok(detail=ShellOutput(output=process.stdout))
    return Result.fail(detail=ShellError(command=command, exit_code=process.returncode,
                                         stdout=process.stdout, stderr=process.stderr))
