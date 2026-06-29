from fastapi import APIRouter
from quantum_core.core.responses import APIResponse

router = APIRouter()

@router.get("/")
def root():
    return APIResponse.success(
        message="Quantum Core running",
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
    from quantum_core.core.exceptions import AppException
    raise AppException(
        message="Test exception"
    )


# REMOVE BEFORE PRODUCTION
@router.get("/crash")
def crash():
    raise Exception(
        "Hidden debug info"
    )