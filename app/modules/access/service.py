from sqlalchemy.orm import Session

from app.modules.users.models import User
from app.modules.access.models import Role, Permission
from app.core.exceptions import AppException


class AccessService:

    # =====================================================
    # ROLE MANAGEMENT
    # =====================================================

    @staticmethod
    def get_role_by_name(db: Session, name: str):
        return db.query(Role).filter(Role.name == name).first()

    @staticmethod
    def create_role(db: Session, name: str, description: str | None = None):
        role = Role(name=name, description=description)
        db.add(role)
        db.commit()
        db.refresh(role)
        return role

    @staticmethod
    def assign_role_to_user(db: Session, user: User, role_name: str):

        role = AccessService.get_role_by_name(db, role_name)

        if not role:
            raise AppException("Role not found", 404)

        if role not in user.roles:
            user.roles.append(role)
            db.commit()
            db.refresh(user)

        return user

    @staticmethod
    def get_user_roles(user: User):
        return [role.name for role in user.roles]

    # =====================================================
    # PERMISSIONS
    # =====================================================

    @staticmethod
    def get_permission_by_name(db: Session, name: str):
        return db.query(Permission).filter(Permission.name == name).first()

    @staticmethod
    def create_permission(db: Session, name: str, description: str | None = None):
        perm = Permission(name=name, description=description)
        db.add(perm)
        db.commit()
        db.refresh(perm)
        return perm

    @staticmethod
    def assign_permission_to_role(db: Session, role: Role, permission_name: str):

        perm = AccessService.get_permission_by_name(db, permission_name)

        if not perm:
            raise AppException("Permission not found", 404)

        if perm not in role.permissions:
            role.permissions.append(perm)
            db.commit()
            db.refresh(role)

        return role

    @staticmethod
    def get_role_permissions(role: Role):
        return [p.name for p in role.permissions]

    # =====================================================
    # AUTHORIZATION CHECKS (CORE ENGINE)
    # =====================================================

    @staticmethod
    def user_has_role(user: User, role_name: str) -> bool:
        return any(role.name == role_name for role in user.roles)

    @staticmethod
    def user_has_permission(user: User, permission_name: str) -> bool:
        return any(
            p.name == permission_name
            for role in user.roles
            for p in role.permissions
        )