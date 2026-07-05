"""
BaseAPI Module Registry

Responsible for discovering, validating,
ordering and loading framework modules.
"""

from pathlib import Path
from importlib import import_module

from app.core.logging import logger

from app.core.exceptions import (
    ModuleLoadError,
    ModuleDependencyError,
    ModuleContractError,
    ModuleRegistrationError,
)

MODULES_PATH = Path(__file__).parent.parent / "modules"

REQUIRED_FIELDS = (
    "NAME",
    "VERSION",
    "DESCRIPTION",
    "AUTHOR",
    "LICENSE",
    "ENABLED",
    "DEPENDENCIES",
    "register",
)


# =====================================================
# Discovery
# =====================================================

def discover_modules():

    modules = []

    if not MODULES_PATH.exists():
        raise FileNotFoundError(MODULES_PATH)

    for item in MODULES_PATH.iterdir():

        if not item.is_dir():
            continue

        if not (item / "__init__.py").exists():
            continue

        modules.append(item.name)

    return sorted(modules)


# =====================================================
# Loading
# =====================================================

def load_module(module_name):

    try:

        return import_module(
            f"app.modules.{module_name}"
        )

    except Exception as exc:

        raise ModuleLoadError(
            f"Unable to import '{module_name}'"
        ) from exc


# =====================================================
# Contract Validation
# =====================================================

def validate_contract(module):

    for field in REQUIRED_FIELDS:

        if not hasattr(module, field):

            raise ModuleContractError(
                f"{module.__name__} missing '{field}'"
            )


# =====================================================
# Dependency Validation
# =====================================================

def validate_dependencies(modules):

    for name, module in modules.items():

        dependencies = getattr(
            module,
            "DEPENDENCIES",
            [],
        )

        for dependency in dependencies:

            if dependency not in modules:

                raise ModuleDependencyError(
                    f"{name} requires '{dependency}'"
                )


# =====================================================
# Dependency Ordering
# =====================================================

def resolve_load_order(modules):

    ordered = []
    visited = set()

    def visit(name):

        if name in visited:
            return

        module = modules[name]

        dependencies = getattr(
            module,
            "DEPENDENCIES",
            [],
        )

        for dependency in dependencies:

            if dependency in modules:
                visit(dependency)

        visited.add(name)
        ordered.append(name)

    for module in modules:
        visit(module)

    return ordered


# =====================================================
# Registration
# =====================================================

def initialize_module(module):

    if hasattr(module, "initialize"):
        module.initialize()


def register_module(app, module):

    try:

        module.register(app)

    except Exception as exc:

        raise ModuleRegistrationError(
            f"Failed registering '{module.NAME}'"
        ) from exc


# =====================================================
# Runtime Lifecycle
# =====================================================

def startup_modules(app, modules):

    logger.info("========== Module Startup ==========")

    for module in modules.values():

        if not getattr(module, "ENABLED", True):
            continue

        if hasattr(module, "startup"):

            try:

                module.startup(app)

                logger.info(
                    "Started %s",
                    module.NAME,
                )

            except Exception:

                logger.exception(
                    "Startup failed: %s",
                    module.NAME,
                )


def shutdown_modules(app, modules):

    logger.info("========== Module Shutdown ==========")

    for module in modules.values():

        if not getattr(module, "ENABLED", True):
            continue

        if hasattr(module, "shutdown"):

            try:

                module.shutdown(app)

                logger.info(
                    "Stopped %s",
                    module.NAME,
                )

            except Exception:

                logger.exception(
                    "Shutdown failed: %s",
                    module.NAME,
                )


# =====================================================
# Loader
# =====================================================

def load_modules(app):

    logger.info("========== BaseAPI Module Loader ==========")

    module_names = discover_modules()

    logger.info(
        "Discovered %s modules",
        len(module_names),
    )

    modules = {}

    for name in module_names:

        try:

            module = load_module(name)

            validate_contract(module)

            modules[name] = module

            logger.info(
                "Loaded %s",
                name,
            )

        except Exception:

            logger.exception(
                "Skipping module '%s'",
                name,
            )

    validate_dependencies(modules)

    order = resolve_load_order(modules)

    logger.info(
        "Load order: %s",
        ", ".join(order),
    )

    ordered_modules = {}

    for name in order:

        module = modules[name]

        if not module.ENABLED:

            logger.info(
                "Disabled %s",
                module.NAME,
            )
            continue

        initialize_module(module)

        register_module(app, module)

        ordered_modules[name] = module

        logger.info(
            "Registered %s",
            module.NAME,
        )

    logger.info(
        "Registered %s modules",
        len(ordered_modules),
    )

    return ordered_modules