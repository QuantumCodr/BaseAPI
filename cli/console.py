import sys


class Console:

    @staticmethod
    def banner():

        print(
            """
==========================================
              BaseAPI CLI
==========================================
"""
        )


    @staticmethod
    def info(message: str):

        print(
            f"[INFO] {message}"
        )


    @staticmethod
    def success(message: str):

        print(
            f"[OK]   {message}"
        )


    @staticmethod
    def warning(message: str):

        print(
            f"[WARN] {message}"
        )


    @staticmethod
    def error(message: str):

        print(
            f"[ERROR] {message}",
            file=sys.stderr
        )


console = Console()