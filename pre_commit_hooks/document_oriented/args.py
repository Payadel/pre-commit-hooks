import argparse
from typing import List, Optional, Sequence

from on_rails import Result, ValidationError, def_result


@def_result()
def get_args(args: Optional[Sequence[str]] = None) -> Result[argparse.ArgumentParser]:
    parser = argparse.ArgumentParser(description='If the source file changes, at least one document must be updated.')
    parser.add_argument('-d', '--doc', action='append', dest='docs', help='docs pattern')
    parser.add_argument('-s', '--source', action='append', dest='sources', help='Source pattern')
    return Result.ok(parser.parse_args(args))


@def_result()
def validate_args(doc_patterns: List[str], src_patterns: List[str]) -> Result:
    # Ensure inputs are specified
    doc_patterns = doc_patterns or []
    if len(doc_patterns) == 0:
        return Result.fail(ValidationError(message='At least one document pattern must be specified.'))

    src_patterns = src_patterns or []
    if len(src_patterns) == 0:
        return Result.fail(ValidationError(message='At least one source pattern must be specified.'))
    return Result.ok()
