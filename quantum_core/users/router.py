from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from quantum_core.database.session import get_db
from quantum_core.users.schemas import UserCreate, UserResponse
from quantum_core.users.service import UserService
from quantum_core.core.responses import APIResponse


router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):

    created_user = UserService.create_user(
        db=db,
        email=user.email,
        password=user.password
    )

    return APIResponse.success(
        message="User created successfully",
        data=UserResponse.from_orm(created_user)
    )