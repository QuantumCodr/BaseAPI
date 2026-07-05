# BaseAPI Module System

The BaseAPI Module System is the foundation of the framework's architecture.

Instead of manually importing routers and configuring modules inside `main.py`, BaseAPI automatically discovers, validates, orders, and registers every module in your application.

This allows developers to build independent features that integrate into the framework with minimal configuration.

---

# Why a Module System?

As applications grow, manually maintaining imports and registrations becomes increasingly difficult.

Every new feature requires changes in multiple places:

* Importing routers
* Registering routers
* Managing dependencies
* Keeping startup order correct
* Remembering to update `main.py`

BaseAPI removes this repetitive work by automatically managing modules for you.

---

# Features

## Automatic Discovery

BaseAPI automatically scans the `app/modules` directory.

Every folder containing an `__init__.py` file is considered a valid module.

No manual registration is required.

---

## Automatic Registration

Each module registers itself with the framework through a single function.

```python
def register(app):
    ...
```

The registry automatically calls this function during application startup.

---

## Module Contracts

Every module follows a common contract.

```python
NAME = "auth"

VERSION = "1.0.0"

DESCRIPTION = "Authentication module"

AUTHOR = "Quantum Core"

LICENSE = "Apache-2.0"

ENABLED = True

DEPENDENCIES = []

def register(app):
    ...
```

Using a standard contract ensures every module behaves consistently across the framework.

---

## Dependency Management

Modules can declare other modules they depend on.

Example:

```python
DEPENDENCIES = [
    "auth",
    "users"
]
```

Before loading modules, BaseAPI validates that every dependency exists.

If a dependency is missing, the framework stops with a clear error instead of failing later at runtime.

---

## Automatic Load Ordering

Modules are automatically loaded in dependency order.

For example:

```
auth
↓

users
↓

access
↓

system
```

This guarantees that dependent modules are never initialized before the modules they require.

Developers never need to manually control load order.

---

## Module Validation

Before a module is registered, BaseAPI validates its contract.

Checks include:

* Required metadata
* Registration function
* Dependency declarations
* Module configuration

Invalid modules are detected immediately during startup.

---

## Enable or Disable Modules

Modules can be disabled without deleting code.

```python
ENABLED = False
```

Disabled modules are ignored by the registry and are not registered with the application.

This makes it easy to temporarily disable features during development or testing.

---

## Logging

Every module action is logged during startup.

Typical startup output:

```
========== BaseAPI Module Loader ==========

Discovered 4 modules

Loaded auth

Loaded users

Loaded access

Loaded system

Load order:
auth
users
access
system

Registered auth

Registered users

Registered access

Registered system

Registered 4 modules
```

These logs help developers quickly identify loading issues, missing dependencies, or disabled modules.

---

# Project Structure

A typical BaseAPI module looks like this.

```text
modules/

└── auth/
    ├── __init__.py
    ├── router.py
    ├── service.py
    ├── schemas.py
    ├── models.py
    ├── dependencies.py
    ├── permissions.py
```

The framework does not enforce every file.

Each module only contains the files it actually needs.

---

# Creating a Module

Create a new folder inside `app/modules`.

Example:

```text
modules/

└── products/
```

Inside the module, define the module contract.

```python
NAME = "products"

VERSION = "1.0.0"

DESCRIPTION = "Product management"

AUTHOR = "Your Name"

LICENSE = "Apache-2.0"

ENABLED = True

DEPENDENCIES = []

def register(app):
    app.include_router(router)
```

Once created, BaseAPI automatically discovers and registers it.

No changes to `main.py` are required.

---

# Current Lifecycle

BaseAPI currently uses a simple lifecycle.

```
Discover Modules
        ↓
Import Modules
        ↓
Validate Contracts
        ↓
Validate Dependencies
        ↓
Resolve Load Order
        ↓
Register Modules
        ↓
Application Starts
```

This keeps the framework lightweight while still providing automatic module management.

---

# Future Roadmap

The Module System will continue evolving.

Planned improvements include:

* Module CLI generation
* External plugin support
* Installable community modules
* Module marketplace
* Hot-pluggable extensions
* Runtime module management

The goal is to allow developers to build reusable features that can be shared across multiple BaseAPI projects.

---

# Philosophy

Each module should represent a single business feature.

Examples include:

* Authentication
* Users
* Payments
* Notifications
* Inventory
* Reports

A module should be self-contained, reusable, and independent whenever possible.

The Module System allows BaseAPI to scale from small applications to large enterprise systems without requiring changes to the framework's core.
