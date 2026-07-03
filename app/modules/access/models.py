from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Table
)

from sqlalchemy.orm import relationship

from app.database.base import Base


# ==========================================
# Users <-> Roles
# ==========================================

user_roles = Table(
    "user_roles",
    Base.metadata,

    Column(
        "user_id",
        Integer,
        ForeignKey(
            "users.id",
            ondelete="CASCADE"
        ),
        primary_key=True
    ),

    Column(
        "role_id",
        Integer,
        ForeignKey(
            "roles.id",
            ondelete="CASCADE"
        ),
        primary_key=True
    )
)


# ==========================================
# Roles <-> Permissions
# ==========================================

role_permissions = Table(
    "role_permissions",
    Base.metadata,

    Column(
        "role_id",
        Integer,
        ForeignKey(
            "roles.id",
            ondelete="CASCADE"
        ),
        primary_key=True
    ),

    Column(
        "permission_id",
        Integer,
        ForeignKey(
            "permissions.id",
            ondelete="CASCADE"
        ),
        primary_key=True
    )
)


# ==========================================
# Roles
# ==========================================

class Role(Base):

    __tablename__ = "roles"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String,
        unique=True,
        nullable=False,
        index=True
    )

    description = Column(
        String,
        nullable=True
    )

    users = relationship(
        "User",
        secondary=user_roles,
        back_populates="roles"
    )

    permissions = relationship(
        "Permission",
        secondary=role_permissions,
        back_populates="roles"
    )


# ==========================================
# Permissions
# ==========================================

class Permission(Base):

    __tablename__ = "permissions"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String,
        unique=True,
        nullable=False,
        index=True
    )

    description = Column(
        String,
        nullable=True
    )

    roles = relationship(
        "Role",
        secondary=role_permissions,
        back_populates="permissions"
    )
