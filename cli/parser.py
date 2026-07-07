from argparse import ArgumentParser

from cli.commands import version
from cli.commands import doctor


def create_parser():

    parser = ArgumentParser(
        prog="baseapi"
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True
    )

    version.register(subparsers)
    doctor.register(subparsers)

    return parser