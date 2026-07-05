from fastapi import Request
from fastapi import HTTPException
from fastapi.exceptions import RequestValidationError

from app.core.responses import APIResponse
from app.core.logging import logger


class AppException(Exception):

    def __init__(
        self,
        message: str,
        status_code: int = 400,
        errors=None
    ):
        self.message = message
        self.status_code = status_code
        self.errors = errors or []


# =====================================================
# Framework Exceptions
# =====================================================

class ModuleError(Exception):
    """Base exception for BaseAPI module system."""


class ModuleLoadError(ModuleError):
    """Raised when a module cannot be imported."""


class ModuleDependencyError(ModuleError):
    """Raised when module dependencies are invalid."""


class ModuleContractError(ModuleError):
    """Raised when a module violates the BaseAPI contract."""


class ModuleRegistrationError(ModuleError):
    """Raised when register() fails."""


# =====================================================
# HTTP Exception Handlers
# =====================================================

async def app_exception_handler(
    request: Request,
    exc: AppException
):

    logger.warning(exc.message)

    return APIResponse.error(
        message=exc.message,
        errors=exc.errors,
        status_code=exc.status_code
    )


async def http_exception_handler(
    request: Request,
    exc: HTTPException
):

    logger.warning(str(exc.detail))

    return APIResponse.error(
        message=str(exc.detail),
        status_code=exc.status_code
    )


async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):

    logger.warning("Validation failed")

    return APIResponse.error(
        message="Validation failed",
        errors=exc.errors(),
        status_code=422
    )


async def generic_exception_handler(
    request: Request,
    exc: Exception
):

    logger.exception(str(exc))

    return APIResponse.error(
        message="Internal server error",
        status_code=500
    )