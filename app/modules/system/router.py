from fastapi import APIRouter
from app.core.responses import APIResponse

router = APIRouter()

@router.get("/")
def root():
    return APIResponse.success(
        message="BaseAPI running",
        data={
            "version": "1.0.0"
        }
    )


@router.get("/health")
def health():
    return APIResponse.success(
        message="System healthy"
    )


# REMOVE BEFORE PRODUCTION
@router.get("/error")
def error():
    from app.core.exceptions import AppException
    raise AppException(
        message="Test exception"
    )


# REMOVE BEFORE PRODUCTION
@router.get("/crash")
def crash():
    raise Exception(
        "Hidden debug info"
    )