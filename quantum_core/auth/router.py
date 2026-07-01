from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from quantum_core.database.session import get_db

from quantum_core.core.responses import APIResponse

from quantum_core.auth.schemas import *

from quantum_core.auth.service import (
    AuthService
)

from quantum_core.auth.dependencies import (
    get_current_user_id
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/register")
def register(
    body: RegisterRequest,
    db: Session = Depends(get_db)
):
 
    user = (
        AuthService.register(
            db,
            body.email,
            body.password
        )
    )

    return APIResponse.success(
        message="Registered",
        data={
            "id": user.id,
            "email": user.email
        }
    )


@router.post("/login")
def login(
    body: LoginRequest,
    db: Session = Depends(get_db)
):

    token = (
        AuthService.login(
            db,
            body.email,
            body.password
        )
    )

    return APIResponse.success(
        data={
            "access_token": token
        }
    )


@router.get("/me")
def me(
    user_id=Depends(
        get_current_user_id
    )
):

    return APIResponse.success(
        data={
            "user_id": user_id
        }
    )


@router.post("/logout")
def logout():
    AuthService.logout()
    return APIResponse.success(
        message="Logged out"
    )

@router.post("/refresh")
def refresh(
    user_id=Depends(
        get_current_user_id
    )
):

    token = (
        AuthService
        .refresh(
            user_id
        )
    )

    return APIResponse.success(
        data={
            "access_token": token
        }
    )

@router.post(
    "/forgot-password"
)
def forgot_password(
    body:
    ForgotPasswordRequest,

    db:
    Session
    =
    Depends(get_db)
):

    token = (
        AuthService
        .forgot_password(
            db,
            body.email
        )
    )

    return APIResponse.success(
        message="Reset token created",
        data={
            "token": token
        }
    )

@router.post(
    "/reset-password"
)
def reset_password(
    body:
    ResetPasswordRequest,

    db:
    Session
    =
    Depends(get_db)
):

    AuthService.reset_password(
        db,
        body.token,
        body.password
    )

    return APIResponse.success(
        message="Password updated"
    )

@router.post(
    "/verify-email"
)
def verify_email(
    body:
    VerifyEmailRequest,

    db:
    Session
    =
    Depends(get_db)
):

    AuthService.verify_email(
        db,
        body.token
    )

    return APIResponse.success(
        message="Email verified"
    )

@router.post(
    "/resend-verification"
)
def resend_verification(

    body:
    ResendVerificationRequest,

    db:
    Session
    =
    Depends(get_db)

):

    AuthService.resend_verification(
        db,
        body.email
    )

    return APIResponse.success(
        message=(
            "Verification email sent"
        )
    )