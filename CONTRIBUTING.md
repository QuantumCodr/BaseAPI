# CONTRIBUTING

Thank you for contributing.

The objective is to keep BaseAPI understandable, reusable, and easy to extend.

---

## Principles

Prefer:

* Simple code
* Clear naming
* Small functions
* Modular design

Avoid:

* Hidden abstractions
* Unused architecture
* Premature optimization

---

## Folder Responsibilities

### auth/

Authentication only.

Examples:

* register
* login
* token logic

Do not place user profile logic here.

---

### users/

User account management.

Examples:

* profile
* account data
* user queries

---

### database/

Database infrastructure only.

Examples:

* sessions
* migrations
* models registration

No business logic.

---

### core/

Shared framework systems.

Examples:

* config
* responses
* exceptions
* security

---

### utils/

Reusable helper functions.

Keep pure and generic.

---

## Coding Rules

Use:

```plaintext
models.py
schemas.py
service.py
router.py
dependencies.py
```

Service:

* business logic

Router:

* HTTP only

Schemas:

* validation only

Models:

* persistence only

---

## Adding New Modules

Example:

```plaintext
payments/
bookings/
inventory/
```

Module template:

```plaintext
module/
models.py
schemas.py
service.py
router.py
dependencies.py
```

Register router in application startup.

---

## Adding User Fields

Update:

```plaintext
users/models.py
users/schemas.py
```

Generate migration:

```bash
python -m alembic revision --autogenerate -m "describe change"
```

Apply:

```bash
python -m alembic upgrade head
```

---

## Database Rules

Never edit applied migrations.

Create new migrations.

Use descriptive migration names.

---

## Pull Request Checklist

Before submitting:

* Code runs
* Tests pass
* Migrations apply
* No secrets committed
* Documentation updated

---

## Goal

Make the framework easier to adopt after every contribution.
