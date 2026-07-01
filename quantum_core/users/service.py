from sqlalchemy.orm import Session

from quantum_core.users.models import User
from quantum_core.core.exceptions import AppException


class UserService:

    @staticmethod
    def get_by_email(
        db: Session,
        email: str
    ):

        return (
            db.query(User)
            .filter(User.email == email)
            .first()
        )

    @staticmethod
    def get_by_id(
        db: Session,
        user_id: int
    ):

        return (
            db.query(User)
            .filter(User.id == user_id)
            .first()
        )

    @staticmethod
    def create(
        db,
        email,
        password_hash,
        verification_token=None,
        is_verified=False
    ):

        user = User(
            email=email,
            password_hash=password_hash,
            verification_token=verification_token,
            is_verified=is_verified
        )

        db.add(user)

        db.commit()

        db.refresh(user)

        return user

    @staticmethod
    def update(
        db: Session,
        user_id: int,
        email: str | None
    ):

        user = (
            UserService
            .get_by_id(
                db,
                user_id
            )
        )

        if not user:

            raise AppException(
                message="User not found",
                status_code=404
            )

        if email:

            user.email = email

        db.commit()

        db.refresh(user)

        return user

    @staticmethod
    def delete(
        db: Session,
        user_id: int
    ):

        user = (
            UserService
            .get_by_id(
                db,
                user_id
            )
        )

        if not user:

            raise AppException(
                message="User not found",
                status_code=404
            )

        db.delete(user)

        db.commit()