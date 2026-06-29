from typing import Any

from fastapi.responses import JSONResponse


class APIResponse:

    @staticmethod
    def success(
        message: str = "Success",
        data: Any = None,
        meta: dict | None = None,
        status_code: int = 200
    ):

        return JSONResponse(
            status_code=status_code,
            content={
                "success": True,
                "message": message,
                "data": data,
                "meta": meta or {}
            }
        )

    @staticmethod
    def error(
        message: str,
        errors: list | None = None,
        meta: dict | None = None,
        status_code: int = 400
    ):

        return JSONResponse(
            status_code=status_code,
            content={
                "success": False,
                "message": message,
                "errors": errors or [],
                "meta": meta or {}
            }
        )