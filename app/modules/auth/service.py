from uuid import uuid4

from app.core.security import (
    hash_password,
    verify_password,
    create_access_token
)

from app.core.exceptions import AppException
from app.modules.users.service import UserService

from app.shared.email import send_email


class AuthService:

    @staticmethod
    def register(db, email, password):

        existing = UserService.get_by_email(db, email)
        if existing:
            raise AppException("User already exists", 409)

        verification_token = str(uuid4())

        user = UserService.create(
            db,
            email,
            hash_password(password),
            verification_token=verification_token,
            is_verified=False
        )

        send_email(
            to=user.email,
            subject="Verify Email",
            body=f"Your verification token:\n\n{verification_token}"
        )

        return user

    @staticmethod
    def login(db, email, password):

        user = UserService.get_by_email(db, email)

        if not user or not verify_password(password, user.password_hash):
            raise AppException("Invalid credentials", 401)

        return create_access_token(user.id)

    @staticmethod
    def forgot_password(db, email):

        user = UserService.get_by_email(db, email)
        if not user:
            return

        token = str(uuid4())
        user.reset_token = token
        db.commit()

        return token

    @staticmethod
    def reset_password(db, token, password):

        user = UserService.get_by_reset_token(db, token)

        if not user:
            raise AppException("Invalid token", 400)

        user.password_hash = hash_password(password)
        user.reset_token = None
        db.commit()

    @staticmethod
    def verify_email(db, token):

        user = UserService.get_by_verification_token(db, token)

        if not user:
            raise AppException("Invalid token", 400)

        user.is_verified = True
        user.verification_token = None
        db.commit()

    @staticmethod
    def resend_verification(db, email):

        user = UserService.get_by_email(db, email)

        if not user:
            raise AppException("User not found", 404)

        if user.is_verified:
            raise AppException("Already verified", 400)

        token = str(uuid4())
        user.verification_token = token
        db.commit()

        send_email(
            to=user.email,
            subject="Verify Email",
            body=f"Your verification token:\n\n{token}"
        )

        return token