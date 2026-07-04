"""
Command Registry

Keeps track of every CLI command available.

All commands should be registered here.
"""

from cli.commands.version import run_version
from cli.commands.doctor import run_doctor
from cli.commands.create import run_create


COMMANDS = {
    "version": run_version,
    "doctor": run_doctor,
    "create": run_create,
}


def get_command(name: str):
    """
    Return a command handler.

    Returns None if command does not exist.
    """
    return COMMANDS.get(name)


def list_commands():
    """
    Return all registered commands.
    """
    return sorted(COMMANDS.keys())