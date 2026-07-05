"""
BaseAPI Module Registry

Responsible for discovering, validating,
ordering and registering framework modules.
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

        if (
            item.is_dir()
            and (item / "__init__.py").exists()
        ):
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

        for dependency in module.DEPENDENCIES:

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

        for dependency in modules[name].DEPENDENCIES:

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

def register_module(app, module):

    try:

        module.register(app)

    except Exception as exc:

        raise ModuleRegistrationError(
            f"Failed registering '{module.NAME}'"
        ) from exc


# =====================================================
# Loader
# =====================================================

def load_modules(app):

    logger.info("=" * 35)
    logger.info("BaseAPI Module Loader")
    logger.info("=" * 35)

    names = discover_modules()

    logger.info(
        "Discovered %s module(s)",
        len(names),
    )

    modules = {}

    for name in names:

        try:

            module = load_module(name)

            validate_contract(module)

            modules[name] = module

        except Exception:

            logger.exception(
                "Skipping '%s'",
                name,
            )

    validate_dependencies(modules)

    order = resolve_load_order(modules)

    logger.info("")
    logger.info("Module Load Order")

    for index, name in enumerate(order, start=1):

        logger.info(
            "%s. %s",
            index,
            name,
        )

    logger.info("")
    logger.info("Registering Modules")

    loaded = 0

    for name in order:

        module = modules[name]

        if not module.ENABLED:

            logger.info(
                "SKIP  %s (disabled)",
                module.NAME,
            )
            continue

        register_module(app, module)

        logger.info(
            "OK    %s",
            module.NAME,
        )

        loaded += 1

    logger.info("")
    logger.info(
        "Framework ready (%s modules loaded)",
        loaded,
    )
    logger.info("=" * 35)

    return modules