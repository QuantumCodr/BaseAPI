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


def require_verified_user(

    user=
    Depends(
        get_current_user
    )

):

    if not user.is_verified:

        raise AppException(
            "Email verification required",
            403
        )

    return user


def require_admin(

    user=
    Depends(
        get_current_user
    )

):

    if getattr(
        user,
        "role",
        None
    ) != "admin":

        raise AppException(
            "Admin required",
            403
        )

    return user


def require_role(
    role
):

    def checker(

        user=
        Depends(
            get_current_user
        )

    ):

        if (
            getattr(
                user,
                "role",
                None
            )
            !=
            role
        ):

            raise AppException(
                "Insufficient permissions",
                403
            )

        return user

    return checker


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