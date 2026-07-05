from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.exceptions import RequestValidationError

from app.core.config import settings
from app.core.registry import load_modules

from app.core.exceptions import (
    AppException,
    app_exception_handler,
    http_exception_handler,
    validation_exception_handler,
    generic_exception_handler,
)

app = FastAPI(
    title=settings.APP_NAME,
    version="v0.1.0-alpha",
)

app.add_exception_handler(
    AppException,
    app_exception_handler,
)

app.add_exception_handler(
    HTTPException,
    http_exception_handler,
)

app.add_exception_handler(
    RequestValidationError,
    validation_exception_handler,
)

app.add_exception_handler(
    Exception,
    generic_exception_handler,
)

load_modules(app)