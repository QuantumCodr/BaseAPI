from cli.services.doctor import DoctorService


def register(subparsers):

    parser = subparsers.add_parser(

        "doctor",

        help="Check project health"

    )

    parser.set_defaults(

        handler=run

    )


def run(args):

    DoctorService().run()