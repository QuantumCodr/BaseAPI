"""
BaseAPI Users Module
"""

from .router import router

NAME = "users"

VERSION = "1.0.0"

DESCRIPTION = "User management module"

ENABLED = True

DEPENDENCIES = []

AUTHOR = "GLEEKAN DAVID WILLIAMS"

LICENSE = "Apache-2.0"


def register(app):
    app.include_router(router)