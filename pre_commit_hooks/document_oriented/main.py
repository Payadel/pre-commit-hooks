#!/usr/bin/env python3

import fnmatch
import sys
from typing import List, Optional, Sequence

from on_rails import ErrorDetail, Result, def_result

from pre_commit_hooks.document_oriented.args import get_args, validate_args
from pre_commit_hooks.document_oriented.git import get_changed_files


@def_result()
def process(changed_files: List[str], source_patterns: List[str], doc_patterns: List[str]) -> Result:
    src_files = [path for path in changed_files if any(fnmatch.fnmatch(path, pattern) for pattern in source_patterns)]
    doc_files = [path for path in changed_files if any(fnmatch.fnmatch(path, pattern) for pattern in doc_patterns)]

    if len(src_files) > 0 and len(doc_files) == 0:
        return Result.fail(ErrorDetail(message=
                                       f'{len(src_files)} source files have been changed. It is necessary to update at least one document file.\n'
                                       f'changed files:\n{src_files}'))
    return Result.ok()


def main(arg_list: Optional[Sequence[str]] = None):
    get_args(arg_list) \
        .on_success_tee(lambda args: validate_args(args.docs, args.sources)) \
        .on_success(lambda args: get_changed_files()
                    .on_success(lambda changed_files: process(changed_files, args.sources, args.docs))
                    ) \
        .on_success(lambda: sys.exit(0)) \
        .on_fail(lambda error: print(error)).on_fail(lambda: sys.exit(1))


if __name__ == '__main__':  # pragma: no cover
    main()
