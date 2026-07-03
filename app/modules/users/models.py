from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Boolean,
    func
)

from app.database.base import Base
from sqlalchemy.orm import relationship


class User(Base):

    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True
    )

    email = Column(
        String,
        unique=True,
        nullable=False,
        index=True
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
        nullable=True,
        index=True
    )

    verification_token = Column(
        String,
        nullable=True,
        index=True
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    roles = relationship(
    "Role",
    secondary="user_roles",
    back_populates="users"
)
