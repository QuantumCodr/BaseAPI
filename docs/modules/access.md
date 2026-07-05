Access Module

The Access module is responsible for role-based access control (RBAC) and permission management in BaseAPI.

It defines how users are authorized to perform actions within the system after they have been authenticated.

The Access module does not handle authentication or user login.

Authentication belongs to the Auth module.

User identity belongs to the Users module.

Access only determines what an authenticated user is allowed to do.

Responsibilities

The Access module is responsible for:

Role management
Permission management
Assigning roles to users
Assigning permissions to roles
Checking user roles
Checking user permissions
Admin access control
Authorization dependencies (guards)

It acts as the authorization engine of BaseAPI.

Core Concept

Access control in BaseAPI follows this model:

User → Roles → Permissions → Access Decision

A user does NOT get permissions directly.

Instead:

Users are assigned roles
Roles contain permissions
Permissions define allowed actions
Module Structure
access/

├── __init__.py
├── models.py
├── schemas.py
├── service.py
├── dependencies.py

Each file has a strict responsibility:

File	Purpose
models.py	Role & Permission database structure
schemas.py	API validation layer
service.py	Business logic
dependencies.py	FastAPI guards
init.py	Module registration
Module Registration

The module is automatically loaded by the BaseAPI module system.

NAME = "access"

VERSION = "1.0.0"

DESCRIPTION = "Role and permission management"

ENABLED = True

DEPENDENCIES = ["auth", "users"]
Registration Entry Point
def register(app):
    pass

The Access module does NOT expose public routes by default.

It is designed as an internal security module.

Database Models

Access defines two core entities:

Roles

A Role represents a user classification.

Examples:

admin
user
manager
editor
Permissions

A Permission represents a specific action.

Examples:

user.read
user.write
role.manage
product.create
Relationships
Many-to-Many: Users ↔ Roles
user_roles

A user can have multiple roles.

A role can belong to multiple users.

Many-to-Many: Roles ↔ Permissions
role_permissions

A role can have multiple permissions.

A permission can belong to multiple roles.

Access Control Flow
Request
   ↓
Authenticated User (Auth Module)
   ↓
Access Dependency Check
   ↓
Role / Permission Validation
   ↓
Allow or Reject Request
Dependency Guards

The Access module provides reusable security dependencies.

require_role(role_name)

Ensures a user has a specific role.

@router.get("/admin")
def admin_route(user=Depends(require_role("admin"))):
    return {"message": "Welcome admin"}
require_permission(permission_name)

Ensures a user has a specific permission.

@router.post("/products")
def create_product(user=Depends(require_permission("product.create"))):
    return {"message": "Product created"}
require_admin()

Shortcut for admin-only routes.

@router.get("/dashboard")
def dashboard(user=Depends(require_admin())):
    return {"message": "Admin dashboard"}
require_verified_user()

Ensures user email is verified.

@router.get("/profile")
def profile(user=Depends(require_verified_user())):
    return {"message": "Verified user only"}
Service Layer

The Access service handles all authorization logic.

Role Management
Create Role

Creates a new role in the system.

AccessService.create_role(db, name="manager")
Assign Role to User
AccessService.assign_role_to_user(db, user, "admin")
Get User Roles
AccessService.get_user_roles(user)
Permission Management
Create Permission
AccessService.create_permission(db, name="user.read")
Assign Permission to Role
AccessService.assign_permission_to_role(db, role, "user.read")
Get Role Permissions
AccessService.get_role_permissions(role)
Authorization Checks
Check Role
AccessService.user_has_role(user, "admin")
Check Permission
AccessService.user_has_permission(user, "user.read")
API Schema Layer

Schemas define how data enters and leaves the system.

Role Schemas
RoleCreate
RoleResponse

Used for:

Creating roles
Returning role data
Permission Schemas
PermissionCreate
PermissionResponse

Used for:

Creating permissions
Returning permission data
Assignment Schemas
AssignRoleRequest
AssignPermissionRequest

Used for:

Assigning roles to users
Assigning permissions to roles
How Access Works in Real Applications
Example 1: Admin Route
@router.get("/admin")
def admin_panel(user=Depends(require_admin())):
    return {"status": "admin access granted"}
Example 2: Permission-Based Access
@router.post("/users")
def create_user(user=Depends(require_permission("user.create"))):
    return {"status": "user created"}
Example 3: Role-Based Access
@router.get("/reports")
def reports(user=Depends(require_role("manager"))):
    return {"status": "manager reports"}
Customizing Access Control

You can extend the system freely.

Add New Roles
roles = [
    "admin",
    "user",
    "manager",
    "support",
    "moderator"
]
Add New Permissions
permissions = [
    "user.read",
    "user.write",
    "order.manage",
    "analytics.view"
]
Dynamic Permission Systems

You can design:

feature-based permissions
API-level permissions
UI-level permissions
multi-tenant roles
Module Relationships
Access Module

│
├── Auth Module
│   └── Provides authenticated user identity
│
├── Users Module
│   └── Provides user data + relationships
│
└── Core Module
    ├── Exceptions
    ├── Database session
    └── Logging
Best Practices

When working with Access:

✔ Always use dependencies instead of manual checks
✔ Never bypass role checks in routers
✔ Keep logic inside service layer
✔ Keep dependencies lightweight
✔ Use permissions for fine-grained control
✔ Use roles for grouping permissions

Design Philosophy

Access is designed to be:

Decoupled from authentication
Independent from business logic
Reusable across all modules
Composable via dependencies
Example Real-World Usage
E-commerce
admin → full access
manager → product + orders
user → own orders only
SaaS App
admin → system control
user → workspace access
billing → subscription permissions
School System
teacher → grade management
student → view only
admin → system control
Summary

The Access module is the authorization engine of BaseAPI.

It determines:

✔ what a user can do
✔ what a user cannot do
✔ how permissions are structured
✔ how security is enforced