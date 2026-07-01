from datetime import datetime
from datetime import timedelta
from uuid import uuid4

from jose import jwt
from passlib.context import CryptContext

from quantum_core.core.config import settings
from quantum_core.core.exceptions import AppException

from quantum_core.users.models import User
from quantum_core.users.service import UserService


pwd = CryptContext(
    schemes=["bcrypt"]
)


class AuthService:

    @staticmethod
    def hash_password(password):
        return pwd.hash(password)

    @staticmethod
    def verify_password(raw, hashed):
        return pwd.verify(raw, hashed)

    @staticmethod
    def create_token(user_id):

        payload = {
            "sub": str(user_id),

            "exp": (
                datetime.utcnow()
                + timedelta(hours=24)
            )
        }

        return jwt.encode(
            payload,
            settings.JWT_SECRET_KEY,
            algorithm="HS256"
        )

    @staticmethod
    def register(
        db,
        email,
        password
    ):

        existing = (
            UserService
            .get_by_email(
                db,
                email
            )
        )

        if existing:

            raise AppException(
                "User already exists",
                409
            )

        verification_token = str(
            uuid4()
        )

        user = (
            UserService
            .create(
                db,
                email,
                AuthService.hash_password(
                    password
                ),
                verification_token=verification_token,
                is_verified=False
            )
        )

        from quantum_core.utils.email import (
            send_email
        )

        send_email(
            to=user.email,
            subject="Verify Email",
            body=(
                "Your verification token:\n\n"
                f"{verification_token}"
            )
        )

        return user

    @staticmethod
    def login(
        db,
        email,
        password
    ):

        user = (
            UserService
            .get_by_email(
                db,
                email
            )
        )

        if not user:

            raise AppException(
                "Invalid credentials",
                401
            )

        if (
            not
            AuthService.verify_password(
                password,
                user.password_hash
            )
        ):

            raise AppException(
                "Invalid credentials",
                401
            )

        return (
            AuthService
            .create_token(
                user.id
            )
        )

    @staticmethod
    def create_reset_token():

        return str(uuid4())

    @staticmethod
    def logout():
        return True
    
    @staticmethod
    def refresh(user_id):

        return (
            AuthService
            .create_token(
                user_id
            )
        )
    
    @staticmethod
    def forgot_password(
        db,
        email
    ):

        user = (
            UserService
            .get_by_email(
                db,
                email
            )
        )

        if not user:
            return

        user.reset_token = (
            AuthService
            .create_reset_token()
        )

        db.commit()

        return user.reset_token
    
    @staticmethod
    def reset_password(
        db,
        token,
        password
    ):

        user = (
            db.query(User)
            .filter(
                User.reset_token
                == token
            )
            .first()
        )

        if not user:

            raise AppException(
                "Invalid token",
                400
            )

        user.password_hash = (
            AuthService
            .hash_password(
                password
            )
        )

        user.reset_token = None

        db.commit()

    @staticmethod
    def verify_email(
        db,
        token
    ):

        user = (
            db.query(User)
            .filter(
                User.verification_token
                == token
            )
            .first()
        )

        if not user:

            raise AppException(
                "Invalid token",
                400
            )

        user.is_verified = True

        user.verification_token = None

        db.commit()

    @staticmethod
    def resend_verification(
        db,
        email
    ):

        user = (
            UserService
            .get_by_email(
                db,
                email
            )
        )

        if not user:

            raise AppException(
                "User not found",
                404
            )

        if user.is_verified:

            raise AppException(
                "Email already verified",
                400
            )

        token = str(
            uuid4()
        )

        user.verification_token = token

        db.commit()

        from quantum_core.utils.email import (
            send_email
        )

        send_email(
            to=user.email,
            subject="Verify Email",
            body=(
                "Your verification token:\n\n"
                f"{token}"
            )
        )

        return token