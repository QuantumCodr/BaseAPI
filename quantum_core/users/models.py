from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Boolean,
    func
)

from quantum_core.database.base import Base


class User(Base):

    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True
    )

    email = Column(
        String,
        unique=True,
        nullable=False
    )

    password_hash = Column(
        String,
        nullable=False
    )

    is_verified = Column(
        Boolean,
        default=False
    )

    reset_token = Column(
        String,
        nullable=True
    )

    verification_token = Column(
        String,
        nullable=True
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )