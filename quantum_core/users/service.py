from sqlalchemy.orm import Session
from passlib.context import CryptContext

from quantum_core.users.models import User
from quantum_core.core.exceptions import AppException


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:

    @staticmethod
    def hash_password(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def create_user(db: Session, email: str, password: str):

        existing = db.query(User).filter(User.email == email).first()

        if existing:
            raise AppException(
                message="User already exists",
                status_code=409
            )

        user = User(
            email=email,
            password_hash=UserService.hash_password(password)
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return user