# Users Module

The Users module is responsible for managing application users within BaseAPI.

It provides the database model, business logic, API endpoints, and schemas required to create, retrieve, update, and delete users.

Unlike the Authentication module, which is responsible for verifying identities and issuing JWT tokens, the Users module manages the user records themselves.

---

# Responsibilities

The Users module is responsible for:

* User database model
* User CRUD operations
* User lookup
* User profile updates
* User deletion
* User response schemas

The module intentionally does **not** perform authentication.

Authentication is handled entirely by the Auth module.

Authorization is handled by the Access module.

Keeping these responsibilities separate makes every module easier to maintain and extend.

---

# Module Structure

```text
users/

├── __init__.py
├── models.py
├── schemas.py
├── service.py
├── router.py
└── base.py
```

Every file has a single responsibility.

---

# Module Registration

Each BaseAPI module exposes metadata inside `__init__.py`.

```python
NAME = "users"

VERSION = "1.0.0"

DESCRIPTION = "User management module"

ENABLED = True

DEPENDENCIES = []

AUTHOR = "GLEEKAN DAVID WILLIAMS

LICENSE = "Apache-2.0"
```

The module is automatically discovered by the BaseAPI Module Registry during application startup.

Registration occurs through the module's register function.

```python
def register(app):
    app.include_router(router)
```

Developers never need to manually edit `main.py` when adding or modifying this module.

---

# Database Model

The Users module owns the `users` database table.

```python
class User(Base):
```

By default the model contains only the fields required by the framework.

Current fields include:

* id
* email
* password_hash
* is_verified
* verification_token
* reset_token
* created_at

This intentionally keeps the framework lightweight while allowing every application to extend the model.

---

# User Roles

A user may have zero or more roles.

The relationship is defined as:

```python
roles = relationship(
    "Role",
    secondary="user_roles",
    back_populates="users"
)
```

The actual Role model belongs to the Access module.

This separation keeps authentication, users, and authorization independent.

---

# Extending the User Model

Every application has different requirements.

Adding additional columns is straightforward.

Example:

```python
first_name = Column(String)

last_name = Column(String)

phone = Column(String)

date_of_birth = Column(Date)

avatar = Column(String)

address = Column(String)
```

After modifying the model, generate a migration.

```bash
alembic revision --autogenerate -m "Add user profile fields"
```

Then apply it.

```bash
alembic upgrade head
```

---

# Schemas

Schemas define how data enters and leaves the API.

Current schemas include:

```text
UserResponse

UserUpdate
```

A larger application may introduce additional schemas such as:

```text
UserCreate

UserProfile

UserList

AdminUserResponse

UserSettings

UserPublicProfile
```

Separating schemas keeps API contracts clean and maintainable.

---

# Service Layer

The service layer contains all business logic.

Current responsibilities include:

* Find user by ID
* Find user by email
* Create user
* Update user
* Delete user

Routes should never contain business logic directly.

Instead they delegate work to the service layer.

Example:

```python
user = UserService.get_by_id(db, user_id)
```

Keeping business logic centralized makes it reusable across routers, background tasks, CLI commands, and future modules.

---

# API Endpoints

The Users router exposes the following endpoints.

```text
GET     /users/{id}

PATCH   /users/{id}

DELETE  /users/{id}
```

Additional endpoints can easily be added.

Examples include:

```text
GET     /users

POST    /users

GET     /users/me

PATCH   /users/me

PATCH   /users/{id}/activate

PATCH   /users/{id}/verify

PATCH   /users/{id}/roles
```

---

# Error Handling

Business logic should raise framework exceptions rather than HTTP exceptions.

Example:

```python
raise AppException(
    message="User not found",
    status_code=404
)
```

The framework automatically converts these exceptions into standardized API responses.

---

# Development Guidelines

When extending the Users module:

* Keep database models inside `models.py`.
* Keep request and response models inside `schemas.py`.
* Keep business logic inside `service.py`.
* Keep HTTP endpoints inside `router.py`.
* Avoid placing business logic inside routes.
* Reuse the service layer whenever possible.
* Raise `AppException` for application errors.

Following these conventions keeps every BaseAPI module consistent.

---

# Module Relationships

The Users module works together with other framework modules.

```text
Users
│
├── Auth
│   ├── Registration
│   ├── Login
│   ├── Password Reset
│   └── JWT Authentication
│
└── Access
    ├── Roles
    ├── Permissions
    └── Authorization
```

The Users module stores user information.

The Auth module verifies identity.

The Access module determines what users are allowed to do.

This separation of concerns is a core design principle of BaseAPI.

---

# Best Practices

When customizing this module:

* Extend rather than replace the User model.
* Keep the model focused on user information.
* Place authentication logic inside the Auth module.
* Place authorization logic inside the Access module.
* Keep services independent from HTTP requests.
* Prefer reusable service methods over duplicated code.

Following these practices keeps applications maintainable while allowing developers to adapt BaseAPI to their own requirements.
