from typing import Optional, Sequence

from on_rails import Result, def_result

from pre_commit_hooks.run_scripts._helpers.argument_helpers import get_args
from pre_commit_hooks.run_scripts._helpers.script_helpers import run_scripts
from pre_commit_hooks.run_scripts._helpers.utility import print_help


def main(args: Optional[Sequence[str]] = None):
    """
    The function runs a program and prints its details and help message if it fails.
    """
    return _run(args=args) \
        .finally_tee(lambda result: print(f"\n{str(result)}")) \
        .on_fail_tee(print_help)


@def_result()
def _run(args: Optional[Sequence[str]] = None) -> Result:
    """
    This function takes arguments, validates them, and runs scripts based on the validated arguments.
    :return: Returning a `Result` object.
    """
    return get_args(args=args) \
        .on_success(lambda value: run_scripts(value[0].file, value[0].directory, value[1]))


# `if __name__ == '__main__':` is a common Python idiom that allows a script to be run as
# the main program or imported as a module. When the script is run as the main program,
# the code block under this condition is executed, which in this case calls the `main()`
# function. If the script is imported as a module, the code block is not executed.
if __name__ == '__main__':  # pragma: no cover
    res = main()
    if res.success:
        raise SystemExit(0)
    raise SystemExit(res.code())
