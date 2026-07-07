import argparse

from cli.commands import version


def create_parser():

    parser = argparse.ArgumentParser(
        prog="baseapi",
        description=(
            "BaseAPI developer CLI"
        )
    )


    subparsers = parser.add_subparsers(
        dest="command"
    )


    version.register(
        subparsers
    )


    return parser