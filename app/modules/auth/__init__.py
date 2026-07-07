"""
BaseAPI Authentication Module
"""

from .router import router

NAME = "auth"

VERSION = "1.0.0"

DESCRIPTION = "Authentication module"

ENABLED = True

DEPENDENCIES = []

AUTHOR = "GLEEKAN DAVID WILLIAMS"

LICENSE = "Apache-2.0"


def register(app):
    app.include_router(router)