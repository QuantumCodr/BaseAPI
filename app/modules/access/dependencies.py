from fastapi import Depends

from app.core.exceptions import AppException
from app.modules.access.service import AccessService
from app.modules.auth.dependencies import get_current_user


# =====================================================
# ROLE CHECKING
# =====================================================

def require_role(role_name: str):
    def checker(user=Depends(get_current_user)):

        if not AccessService.user_has_role(user, role_name):
            raise AppException(
                message="Forbidden: insufficient role",
                status_code=403
            )

        return user

    return checker


# =====================================================
# PERMISSION CHECKING
# =====================================================

def require_permission(permission_name: str):
    def checker(user=Depends(get_current_user)):

        if not AccessService.user_has_permission(user, permission_name):
            raise AppException(
                message="Forbidden: insufficient permission",
                status_code=403
            )

        return user

    return checker


# =====================================================
# ADMIN SHORTCUT
# (optional convenience wrapper)
# =====================================================

def require_admin():
    def checker(user=Depends(get_current_user)):

        if not AccessService.user_has_role(user, "admin"):
            raise AppException(
                message="Admin access required",
                status_code=403
            )

        return user

    return checker


# =====================================================
# VERIFIED USER CHECK
# (belongs here, not auth)
# =====================================================

def require_verified_user():
    def checker(user=Depends(get_current_user)):

        if not user.is_verified:
            raise AppException(
                message="Email verification required",
                status_code=403
            )

        return user

    return checker