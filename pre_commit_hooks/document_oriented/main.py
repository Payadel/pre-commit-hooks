#!/usr/bin/env python3

import argparse
import fnmatch
import subprocess
from typing import List

from on_rails import ErrorDetail, Result, ValidationError, def_result


@def_result()
def get_args() -> Result[argparse.ArgumentParser]:
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='If the source file changes, at least one document must be updated.')
    parser.add_argument('-d', '--doc', action='append', dest='docs', help='docs pattern')
    parser.add_argument('-s', '--source', action='append', dest='sources', help='Source pattern')
    return Result.ok(parser.parse_args())


@def_result()
def validate_args(doc_patterns: List[str], src_patterns: List[str]) -> Result:
    # Ensure inputs are specified
    doc_patterns = doc_patterns or []
    if len(doc_patterns) == 0:
        return Result.fail(ValidationError('At least one document pattern must be specified.'))

    src_patterns = src_patterns or []
    if len(src_patterns) == 0:
        return Result.fail(ValidationError('At least one source pattern must be specified.'))
    return Result.ok()


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
        ["git", "log", "--name-only", "--pretty=format:''", f"{remote_branch_name}..HEAD"],
        universal_newlines=True)) \
        .on_success(lambda changed_files: changed_files.strip().split('\n')) \
        .on_success(lambda changed_files: [file for file in changed_files if len(file.strip()) > 0])


@def_result()
def process(changed_files: List[str], source_patterns: List[str], doc_patterns: List[str]) -> Result:
    # Use fnmatch to select files that match at least one of the patterns
    src_files = [path for path in changed_files if any(fnmatch.fnmatch(path, pattern) for pattern in source_patterns)]
    doc_files = [path for path in changed_files if any(fnmatch.fnmatch(path, pattern) for pattern in doc_patterns)]

    if len(src_files) > 0 and len(doc_files) == 0:
        return Result.fail(ErrorDetail(
            f'{len(src_files)} source files have been changed. It is necessary to update at least one document file.\n'
            f'changed files:\n{src_files}'))
    return Result.ok()


def main():
    get_args() \
        .on_success_tee(lambda args: validate_args(args.docs, args.sources)) \
        .on_success(lambda args: get_changed_files()
                    .on_success(lambda changed_files: process(changed_files, args.sources, args.docs))
                    ) \
        .on_success(lambda: exit(0)) \
        .on_fail(lambda error: print(error)).on_fail(lambda: exit(1))


if __name__ == '__main__':
    main()
