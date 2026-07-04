"""
CLI Argument Parser

Responsible for converting raw command-line arguments
into a structured command request.
"""


class CommandRequest:
    """
    Represents a parsed CLI command.
    """

    def __init__(self, command, arguments=None, options=None):
        self.command = command
        self.arguments = arguments or []
        self.options = options or {}


def parse(argv):
    """
    Parse command-line arguments.

    Example:

    Input:
        ["create", "shop", "--docker"]

    Output:
        CommandRequest(
            command="create",
            arguments=["shop"],
            options={
                "docker": True
            }
        )
    """

    if not argv:
        return None

    command = argv[0]

    arguments = []
    options = {}

    for item in argv[1:]:

        if item.startswith("--"):
            options[item[2:]] = True

        else:
            arguments.append(item)

    return CommandRequest(
        command=command,
        arguments=arguments,
        options=options,
    )