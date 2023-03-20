import os
import subprocess
from typing import List

from pre_commit_hooks.libs.Details import RunShellErrorDetail, SuccessDetail
from pre_commit_hooks.libs.Result import Result


class Utility:
    @staticmethod
    def get_arg(args: List[str], index: int, default="") -> str:
        if len(args) > index:
            return args[index]
        return default

    @staticmethod
    def get_file_name(file_path: str) -> str:
        return os.path.basename(file_path)

    @staticmethod
    def run_shell(commands: List[str]) -> Result:
        process = subprocess.run(commands, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False, shell=True)
        if process.returncode == 0:
            return Result.ok(SuccessDetail(message=process.stdout.decode("utf-8")))
        return Result.fail(
            RunShellErrorDetail(message=process.stderr.decode("utf-8"), output=process.stdout.decode("utf-8")))

    @staticmethod
    def get_sorted_scripts(directory: str) -> List[str]:
        scripts = os.listdir(directory)
        scripts.sort()
        return [os.path.join(directory, script) for script in scripts]
