from pydantic import BaseModel


class RoleCreate(BaseModel):
    name: str
    description: str | None = None


class RoleResponse(BaseModel):
    id: int
    name: str
    description: str | None = None

    class Config:
        from_attributes = True


class PermissionCreate(BaseModel):
    name: str
    description: str | None = None


class PermissionResponse(BaseModel):
    id: int
    name: str
    description: str | None = None

    class Config:
        from_attributes = True


class AssignRoleRequest(BaseModel):
    user_id: int
    role_name: str


class AssignPermissionRequest(BaseModel):
    role_name: str
    permission_name: str