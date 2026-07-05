NAME = "access"

VERSION = "1.0.0"

DESCRIPTION = "Role and permission management"

ENABLED = True

DEPENDENCIES = [
    "auth",
    "users",
]

AUTHOR = "Quantum Core"

LICENSE = "Apache-2.0"


def register(app):
    """
    Access currently exposes no API routes.
    """
    pass