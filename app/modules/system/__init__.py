"""
BaseAPI System Module
"""

from .router import router

NAME = "system"

VERSION = "1.0.0"

DESCRIPTION = "System health and framework information"

ENABLED = True

DEPENDENCIES = []

AUTHOR = "GLEEKAN DAVID WILLIAMS"

LICENSE = "Apache-2.0"


def register(app):
    app.include_router(router)