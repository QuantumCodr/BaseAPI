from cli.parser import create_parser
from cli.console import console


def main():

    parser = create_parser()

    args = parser.parse_args()


    if hasattr(
        args,
        "handler"
    ):

        #console.banner()

        args.handler(args)

    else:

        parser.print_help()