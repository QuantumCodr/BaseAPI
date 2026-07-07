# Authentication Module

The Authentication module is responsible for verifying user identities and securing access to your application.

It provides user registration, login, JWT authentication, email verification, password recovery, and authenticated user dependencies.

The Authentication module does **not** own user data. User records belong to the Users module, while authorization belongs to the Access module.

---

# Responsibilities

The Authentication module is responsible for:

* User registration
* User login
* JWT access token generation
* Password hashing
* Password verification
* Current authenticated user
* Optional authentication
* Email verification
* Password reset
* Refresh access tokens
* Authentication dependencies

The module intentionally does **not** manage users or permissions.

User management belongs to the Users module.

Role and permission management belongs to the Access module.

---

# Module Structure

```text
auth/

├── __init__.py
├── router.py
├── service.py
├── schemas.py
└── dependencies.py
```

Each file has a single responsibility.

---

# Module Registration

Every BaseAPI module exposes metadata inside `__init__.py`.

```python
NAME = "auth"

VERSION = "1.0.0"

DESCRIPTION = "Authentication module"

ENABLED = True

DEPENDENCIES = []

AUTHOR = "GLEEKAN DAVID WILLIAMS"

LICENSE = "Apache-2.0"
```

The BaseAPI Module Registry automatically discovers and registers this module during application startup.

```python
def register(app):
    app.include_router(router)
```

No manual changes to `main.py` are required.

---

# Authentication Flow

The Authentication module follows a simple flow.

```text
Client

↓

Register/Login Request

↓

Auth Router

↓

Auth Service

↓

Users Module

↓

Database

↓

JWT Token

↓

Authenticated Requests
```

The router accepts requests.

The service performs authentication logic.

The Users module retrieves or creates user records.

The Security utilities generate JWT tokens.

---

# Configuration

Authentication is configured using environment variables.

```env
JWT_SECRET_KEY=your-secret-key

JWT_ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=60

REFRESH_TOKEN_EXPIRE_DAYS=7
```

These settings are loaded through `app.core.config.Settings`.

Never hardcode secret keys into your application.

---

# Password Security

Passwords are never stored in plain text.

BaseAPI uses bcrypt through Passlib.

```python
hash_password(password)

verify_password(raw, hashed)
```

Whenever a new password is created or changed, it is hashed before being stored.

---

# JWT Authentication

Successful login returns a signed JWT access token.

```python
token = create_access_token(user.id)
```

Every protected request includes the token.

```
Authorization: Bearer <access_token>
```

Incoming tokens are decoded using:

```python
decode_token(token)
```

Invalid or expired tokens automatically raise an `AppException`.

---

# Authentication Dependencies

The module provides reusable dependencies for protecting routes.

Current dependencies include:

```text
get_current_user_id()

get_current_user()

optional_auth()
```

These dependencies can be reused across every module in the framework.

Example:

```python
@router.get("/profile")
def profile(
    user=Depends(get_current_user)
):
    ...
```

---

# API Endpoints

The Authentication module exposes the following endpoints.

```text
POST   /auth/register

POST   /auth/login

GET    /auth/me

POST   /auth/logout

POST   /auth/refresh

POST   /auth/forgot-password

POST   /auth/reset-password

POST   /auth/verify-email

POST   /auth/resend-verification
```

These endpoints provide the complete authentication lifecycle for most applications.

---

# Registration

User registration performs the following steps.

1. Check if the email already exists.
2. Hash the password.
3. Generate a verification token.
4. Create the user using the Users module.
5. Send a verification email.
6. Return the newly created user.

The Authentication module never inserts records directly into the database.

Instead it delegates user creation to the Users module.

---

# Login

Login performs the following checks.

1. Retrieve the user by email.
2. Verify the password hash.
3. Generate a JWT access token.
4. Return the token.

Example response:

```json
{
    "access_token": "<jwt-token>"
}
```

---

# Password Recovery

Password recovery is divided into two operations.

### Forgot Password

Generates a reset token.

Stores the token on the user.

Optionally sends an email.

### Reset Password

Verifies the reset token.

Hashes the new password.

Clears the reset token.

Stores the new password hash.

---

# Email Verification

New users receive a verification token.

The verification endpoint:

* validates the token,
* marks the account as verified,
* removes the verification token.

Verification emails can also be resent when necessary.

---

# Schemas

Request validation is handled using Pydantic schemas.

Current schemas include:

```text
RegisterRequest

LoginRequest

PasswordChangeRequest

ForgotPasswordRequest

ResetPasswordRequest

VerifyEmailRequest

ResendVerificationRequest
```

As the framework grows, additional schemas may be added without affecting existing endpoints.

---

# Service Layer

The service layer contains all authentication business logic.

Current responsibilities include:

* Register
* Login
* Forgot password
* Reset password
* Verify email
* Resend verification

Routers should remain thin and delegate all business logic to the service layer.

---

# Customizing Authentication

Every application has different authentication requirements.

Common customizations include:

* Username login
* Phone number login
* Two-factor authentication (2FA)
* Social authentication
* Multi-factor authentication (MFA)
* Magic link login
* One-time passwords (OTP)
* OAuth providers
* Single Sign-On (SSO)

These features should be implemented inside the Authentication module without modifying the Users module.

---

# Module Relationships

The Authentication module depends on other framework components.

```text
Authentication

│

├── Users
│   ├── User lookup
│   ├── User creation
│   └── User updates
│
├── Core
│   ├── JWT
│   ├── Password hashing
│   ├── Configuration
│   └── Exceptions
│
└── Shared
    └── Email service
```

Authentication authenticates users.

Users stores user records.

Access authorizes authenticated users.

Keeping these concerns separate makes the framework easier to maintain and extend.

---

# Best Practices

When extending this module:

* Never store plain text passwords.
* Always hash passwords before saving.
* Keep JWT generation inside `core.security`.
* Keep business logic inside `service.py`.
* Keep HTTP logic inside `router.py`.
* Reuse the Users module instead of querying the database directly.
* Raise `AppException` for authentication errors.
* Keep authentication independent from authorization.

Following these conventions ensures that the Authentication module remains secure, reusable, and easy to extend across different applications.
