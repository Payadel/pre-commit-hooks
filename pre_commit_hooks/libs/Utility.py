import os
import subprocess
from typing import List

from pre_commit_hooks.libs.Details import RunShellErrorDetail, SuccessDetail
from pre_commit_hooks.libs.Result import Result


class Utility:
    """ Some helper methods """

    @staticmethod
    def get_arg(args: List[str], index: int, default="") -> str:
        """ Get index of list or return default """
        if len(args) > index:
            return args[index]
        return default

    @staticmethod
    def get_file_name(file_path: str) -> str:
        """ Get file name base file path """
        return os.path.basename(file_path)

    @staticmethod
    def run_shell(commands: List[str]) -> Result:
        """ Run a shell command and return result as Result type """
        process = subprocess.run(commands, stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE,
                                 check=False, shell=True)
        if process.returncode == 0:
            return Result.ok(SuccessDetail(message=process.stdout.decode("utf-8")))
        return Result.fail(RunShellErrorDetail(message=process.stderr.decode("utf-8"),
                                               output=process.stdout.decode("utf-8")))

    @staticmethod
    def get_sorted_scripts(directory: str) -> List[str]:
        """ Collect files from directory, sort them and return paths """
        scripts = os.listdir(directory)
        scripts.sort()
        return [os.path.join(directory, script) for script in scripts]
