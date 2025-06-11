"""
`uv` forcefully creates and activates a virtual environment for the project, even if a virtual environment is already activated.
This behavior is not desirable for users who are already using a virtual environment manager like `conda` or `virtualenv`.
To support these users, we have created a wrapper script called `vuv` that will pass all arguments to the `uv` command.
This script will only run the `uv` command if a virtual environment is activated.
If no virtual environment is activated, it will print a message asking the user to activate a virtual environment.


This `uv` wrapper script is needed to support automatic virtual environment support in `uv`.
Related issue: https://github.com/astral-sh/uv/issues/11315
"""

import argparse
import os
import subprocess
import sys


def main():
    """Parse all arguments and pass them to the `uv` command."""

    # Parse all arguments
    parser = argparse.ArgumentParser(description="Run the `uv` command.")
    parser.add_argument("args", nargs=argparse.REMAINDER, help="Arguments to pass to the `uv` command.")
    args = parser.parse_args()

    # Converts `install` command to `sync --inexact` command.
    # This workaround is to match `uv` behavior with `poetry` behavior.
    if args.args and args.args[0] == "install":
        args.args = ["sync", "--inexact"] + args.args[1:]

    # Setup environment variables
    env = os.environ.copy()
    if "CONDA_DEFAULT_ENV" in env and env["CONDA_DEFAULT_ENV"] != "base":
        # to support `project` feature: https://docs.astral.sh/uv/configuration/environment/#uv_project_environment
        env["UV_PROJECT_ENVIRONMENT"] = env["CONDA_PREFIX"]
        # to support `--active` option: https://github.com/astral-sh/uv/pull/11189
        # this is not mandatory
        env["VIRTUAL_ENV"] = env["CONDA_PREFIX"]
    elif "VIRTUAL_ENV" in env:
        # to support `project` feature: https://docs.astral.sh/uv/configuration/environment/#uv_project_environment
        env["UV_PROJECT_ENVIRONMENT"] = env["VIRTUAL_ENV"]
    else:
        # block `uv` command if no virtual environment is activated
        print("Please activate a virtual environment to run the `vuv` command.")
        return 1

    # Run the `uv` command
    result = subprocess.run(["uv"] + args.args, env=env)
    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
