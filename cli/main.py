"""
BaseAPI CLI Entry Point
"""

import sys

from cli.console import error
from cli.parser import parse
from cli.registry import (
    get_command,
    list_commands,
)


def main():

    request = parse(sys.argv[1:])

    if request is None:
        error(
            "No command provided.\n"
            "Try: baseapi doctor"
        )
        sys.exit(1)

    handler = get_command(request.command)

    if handler is None:

        error(
            f"Unknown command '{request.command}'\n\n"
            f"Available commands:\n"
            + "\n".join(
                f"  • {cmd}"
                for cmd in list_commands()
            )
        )

        sys.exit(1)

    handler(request)


if __name__ == "__main__":
    main()