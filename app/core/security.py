from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext

from app.core.config import settings
from app.core.exceptions import AppException

pwd_context = CryptContext(schemes=["bcrypt"])


# ==========================================
# PASSWORDS
# ==========================================

def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(raw: str, hashed: str) -> bool:
    return pwd_context.verify(raw, hashed)


# ==========================================
# JWT
# ==========================================

def create_access_token(user_id: int) -> str:
    payload = {
        "sub": str(user_id),
        "exp": datetime.utcnow() + timedelta(hours=24)
    }

    return jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm="HS256"
    )


def decode_token(token: str) -> dict:
    try:
        return jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=["HS256"]
        )
    except Exception:
        raise AppException("Invalid token", 401)