# BaseAPI

A reusable, production-ready FastAPI backend foundation that lets you start building your application instead of rebuilding backend infrastructure.

BaseAPI provides authentication, role-based authorization, database configuration, standardized API responses, logging, and a scalable modular architecture out of the box.

---

# Why BaseAPI?

Most backend projects begin by recreating the same foundation:

* User authentication
* JWT tokens
* Password hashing
* User management
* Database configuration
* Migrations
* Error handling
* API responses
* Logging
* Role-based permissions

BaseAPI provides these features so you can focus on building your application's business logic.

---

# Features

## Authentication

* User registration
* User login
* JWT authentication
* Password hashing (bcrypt)
* Current authenticated user
* Optional authentication
* Email verification
* Forgot password
* Password reset
* Logout
* Refresh access token

## Authorization (RBAC)

* Roles
* Permissions
* Many-to-many user-role relationship
* Many-to-many role-permission relationship
* Route protection
* Admin shortcut dependency
* Verified user dependency
* Custom role and permission support

## Infrastructure

* PostgreSQL
* SQLAlchemy ORM
* Alembic migrations
* Environment configuration
* Centralized logging
* Standardized API responses
* Global exception handling
* Database seed system
* Feature-first modular architecture

---

# Project Structure

```text
BaseAPI/

├── app/
│
│   ├── main.py
│
│   ├── core/
│   │   ├── config.py
│   │   ├── security.py
│   │   ├── responses.py
│   │   ├── exceptions.py
│   │   ├── logging.py
│   │   └── registry.py
│   │
│   ├── database/
│   │   ├── session.py
│   │   ├── base.py
│   │   └── migrations/
│   │
│   ├── shared/
│   │   ├── email.py
│   │   ├── helpers.py
│   │   ├── validators.py
│   │   ├── constants.py
│   │   └── pagination.py
│   │
│   └── modules/
│       ├── auth/
│       ├── users/
│       └── access/
│
├── docs/
├── logs/
├── scripts/
├── tests/
├── Dockerfile
├── pyproject.toml
└── README.md
```

---

# Installation

Clone the repository.

```bash
git clone https://github.com/QuantumCodr/BaseAPI.git
```

Enter the project.

```bash
cd BaseAPI
```

Create a virtual environment.

```bash
python -m venv .venv
```

Activate it.

Windows

```bash
.venv\Scripts\activate
```

Linux/macOS

```bash
source .venv/bin/activate
```

Install dependencies.

```bash
pip install -r requirements.txt
```

---

# Environment Setup

Copy the example environment file.

```bash
copy .env.example .env
```

Configure your database and application settings inside `.env`.

---

# Database Setup

Run migrations.

```bash
alembic upgrade head
```

---

# Seed Default Roles and Permissions

Populate the database with default roles, permissions, and an administrator account.

```bash
python scripts/seed.py
```

By default, BaseAPI creates:

### Roles

* admin
* user

### Permissions

* user.read
* user.write
* user.delete
* role.manage
* permission.manage
* admin.access

These defaults are fully customizable by editing `scripts/seed.py`.

---

# Run the Development Server

```bash
uvicorn app.main:app --reload
```

Swagger UI

```
http://127.0.0.1:8000/docs
```

ReDoc

```
http://127.0.0.1:8000/redoc
```

---

# Authentication Endpoints

```
POST   /auth/register
POST   /auth/login
POST   /auth/logout
POST   /auth/refresh
POST   /auth/forgot-password
POST   /auth/reset-password
POST   /auth/verify-email
GET    /auth/me
```

---

# Protecting Routes

Require an administrator.

```python
@router.get(
    "/admin",
    dependencies=[Depends(require_admin())]
)
```

Require a role.

```python
@router.get(
    "/reports",
    dependencies=[Depends(require_role("manager"))]
)
```

Require a permission.

```python
@router.post(
    "/products",
    dependencies=[Depends(require_permission("product.create"))]
)
```

Require a verified account.

```python
@router.get(
    "/profile",
    dependencies=[Depends(require_verified_user())]
)
```

---

# Customizing Roles

BaseAPI does not enforce a fixed permission system.

Developers are free to define any roles or permissions that fit their application.

Example:

```python
roles = [
    {
        "name": "manager",
        "permissions": [
            "inventory.read",
            "inventory.write",
            "orders.manage"
        ]
    }
]
```

This makes the framework suitable for e-commerce platforms, school systems, CRMs, healthcare systems, SaaS products, and many other applications.

---

# Testing

Run the test suite.

```bash
pytest
```

---

# Documentation

Additional documentation is available in the `docs/` directory.

Future guides will include:

* Authentication
* Authorization
* Database
* Migrations
* Testing
* Deployment
* CLI
* Plugin Development

---

# Roadmap

## Completed

* Authentication
* JWT
* User Management
* Role-Based Access Control (RBAC)
* PostgreSQL
* SQLAlchemy
* Alembic
* Global Exception Handling
* Standard API Responses
* Logging
* Seed System

## Coming Soon

* Package Publishing (PyPI)
* CLI Project Generator
* Plugin System
* Email Providers
* File Uploads
* Notification Module
* Payment Module
* AI Module
* Background Jobs

---

# Philosophy

BaseAPI provides reusable infrastructure.

Business logic belongs inside your application's modules.

Keep the framework clean, reusable, and easy to extend.

---

# Version

Current Version

```
v0.1.0-alpha
```

---

# License

This project is licensed under the Apache License 2.0.

See the LICENSE file for details.
