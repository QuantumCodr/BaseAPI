from pydantic import BaseModel, EmailStr


# INPUT (what user sends)
class UserCreate(BaseModel):
    email: EmailStr
    password: str


# OUTPUT (what API returns)
class UserResponse(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True