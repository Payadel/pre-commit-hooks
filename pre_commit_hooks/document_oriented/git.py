import subprocess
from typing import List

from on_rails import Result, def_result


@def_result()
def get_remote_branch_name() -> Result[str]:
    return Result.ok(
        subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "@{upstream}"]).decode('utf-8').strip())


@def_result()
def get_changed_files() -> Result[List[str]]:
    return get_remote_branch_name() \
        .on_success_operate_when(lambda remote_branch_name: remote_branch_name == '', lambda: [], break_rails=True) \
        .on_success(lambda remote_branch_name: _get_changed_files(remote_branch_name))


@def_result()
def _get_changed_files(remote_branch_name: str) -> Result[List[str]]:
    return Result.ok().try_func(func=lambda: subprocess.check_output(
        ["git", "log", "--name-only", "--pretty=format:''", f"{remote_branch_name}..HEAD"])) \
        .on_success(lambda changed_files: changed_files.decode('utf-8').strip().split('\n')) \
        .on_success(lambda changed_files: [file for file in changed_files if len(file.strip()) > 0])
