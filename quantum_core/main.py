from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.exceptions import RequestValidationError

from quantum_core.core.config import settings

from quantum_core.core.exceptions import (
    AppException,
    app_exception_handler,
    http_exception_handler,
    validation_exception_handler,
    generic_exception_handler
)

from quantum_core.system.router import router as system_router


app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0"
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