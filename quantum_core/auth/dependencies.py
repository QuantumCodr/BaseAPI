from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from jose import jwt
from quantum_core.core.config import settings
from quantum_core.core.exceptions import AppException

security = HTTPBearer()

def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    try:
        token = credentials.credentials

        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=["HS256"]
        )

        return int(payload["sub"])

    except Exception:
        raise AppException("Invalid token", 401)