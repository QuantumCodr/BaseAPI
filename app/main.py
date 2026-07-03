from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.exceptions import RequestValidationError

from app.core.config import settings

from app.core.exceptions import (
    AppException,
    app_exception_handler,
    http_exception_handler,
    validation_exception_handler,
    generic_exception_handler
)

from app.modules.system.router import router as system_router
from app.modules.users.router import router as users_router
from app.modules.auth.router import router as auth_router

app = FastAPI(
    title=settings.APP_NAME,
    version="v0.1.0-alpha"
)


app.add_exception_handler(
    AppException,
    app_exception_handler
)

app.add_exception_handler(
    HTTPException,
    http_exception_handler
)

app.add_exception_handler(
    RequestValidationError,
    validation_exception_handler
)

app.add_exception_handler(
    Exception,
    generic_exception_handler
)


app.include_router(
    system_router
)

app.include_router(
    users_router
)

app.include_router(
    auth_router
)