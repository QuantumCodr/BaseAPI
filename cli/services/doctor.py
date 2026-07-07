from pathlib import Path
from importlib.metadata import version, PackageNotFoundError
import platform
import sys


class Check:

    def __init__(self, name, passed, message=""):
        self.name = name
        self.passed = passed
        self.message = message


class DoctorService:

    def __init__(self):

        self.project = Path.cwd()

        self.checks = []

    # ==========================================
    # Public
    # ==========================================

    def run(self):

        self.python()

        self.virtualenv()

        self.baseapi()

        self.pyproject()

        self.app()

        self.modules()

        self.env()

        self.summary()

    # ==========================================
    # Checks
    # ==========================================

    def python(self):

        self.checks.append(

            Check(
                "Python",
                True,
                platform.python_version()
            )

        )

    def virtualenv(self):

        active = (
            hasattr(sys, "real_prefix")
            or
            sys.prefix != sys.base_prefix
        )

        self.checks.append(

            Check(
                "Virtual Environment",
                active
            )

        )

    def baseapi(self):

        try:

            v = version("baseapi")

            self.checks.append(

                Check(
                    "BaseAPI",
                    True,
                    v
                )

            )

        except PackageNotFoundError:

            self.checks.append(

                Check(
                    "BaseAPI",
                    False
                )

            )

    def pyproject(self):

        self.checks.append(

            Check(
                "pyproject.toml",
                (
                    self.project /
                    "pyproject.toml"
                ).exists()
            )

        )

    def app(self):

        self.checks.append(

            Check(
                "app/",
                (
                    self.project /
                    "app"
                ).exists()
            )

        )

    def modules(self):

        self.checks.append(

            Check(
                "app/modules/",
                (
                    self.project /
                    "app" /
                    "modules"
                ).exists()
            )

        )

    def env(self):

        self.checks.append(

            Check(
                ".env",
                (
                    self.project /
                    ".env"
                ).exists()
            )

        )

    # ==========================================
    # Output
    # ==========================================

    def summary(self):

        print()

        print("=" * 42)

        print("             BaseAPI Doctor")

        print("=" * 42)

        print()

        healthy = True

        for check in self.checks:

            icon = "✓" if check.passed else "✗"

            if not check.passed:

                healthy = False

            if check.message:

                print(
                    f"{icon} {check.name:<24} {check.message}"
                )

            else:

                print(
                    f"{icon} {check.name}"
                )

        print()

        print("=" * 42)

        print(
            f"Status : {'HEALTHY' if healthy else 'ISSUES FOUND'}"
        )

        print("=" * 42)