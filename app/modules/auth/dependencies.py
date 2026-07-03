from fastapi import Depends
from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials
)

from jose import jwt
from sqlalchemy.orm import Session

from app.database.session import (
    get_db
)

from app.core.config import (
    settings
)

from app.core.exceptions import (
    AppException
)

from app.modules.users.models import (
    User
)

security = HTTPBearer()


def get_current_user_id(

    credentials:
    HTTPAuthorizationCredentials
    =
    Depends(security)

):

    try:

        token = (
            credentials
            .credentials
        )

        payload = jwt.decode(

            token,

            settings.JWT_SECRET_KEY,

            algorithms=[
                "HS256"
            ]
        )

        return int(
            payload["sub"]
        )

    except Exception:

        raise AppException(
            "Invalid token",
            401
        )


def get_current_user(

    user_id:
    int
    =
    Depends(
        get_current_user_id
    ),

    db:
    Session
    =
    Depends(
        get_db
    )

):

    user = (

        db.query(User)

        .filter(
            User.id
            ==
            user_id
        )

        .first()
    )

    if not user:

        raise AppException(
            "User not found",
            404
        )

    return user


def optional_auth(

    credentials:
    HTTPAuthorizationCredentials
    =
    Depends(
        HTTPBearer(
            auto_error=False
        )
    ),

    db:
    Session
    =
    Depends(
        get_db
    )

):

    if not credentials:

        return None

    try:

        payload = jwt.decode(

            credentials.credentials,

            settings.JWT_SECRET_KEY,

            algorithms=[
                "HS256"
            ]
        )

        return (

            db.query(User)

            .filter(
                User.id
                ==
                int(
                    payload["sub"]
                )
            )

            .first()
        )

    except Exception:

        return None