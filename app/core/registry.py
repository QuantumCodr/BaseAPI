"""
BaseAPI Module Registry

Responsible for discovering, validating,
ordering and registering framework modules.
"""

from pathlib import Path
from importlib import import_module

from app.core.logging import logger
from app.core.logging import logger, phase, section, log

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

    # ============================================================
    phase("BASEAPI MODULE LOADER INITIALIZATION")
    # ============================================================

    logger.info("BaseAPI module system starting up...")

    # ============================================================
    section("DISCOVERY PHASE")
    # ============================================================

    names = discover_modules()

    logger.info("Discovered %s module(s)", len(names))
    logger.info("Modules found: %s", ", ".join(names) if names else "None")

    modules = {}

    # ============================================================
    section("VALIDATION + LOADING PHASE")
    # ============================================================

    for name in names:

        try:
            logger.info("Loading module: %s", name)

            module = load_module(name)

            validate_contract(module)

            modules[name] = module

        except Exception:
            logger.exception("Skipping '%s' due to load/validation error", name)

    # ============================================================
    section("DEPENDENCY RESOLUTION PHASE")
    # ============================================================

    validate_dependencies(modules)

    order = resolve_load_order(modules)

    logger.info("Load order resolved:")

    for index, name in enumerate(order, start=1):
        logger.info("%s. %s", index, name)

    # ============================================================
    section("REGISTRATION PHASE")
    # ============================================================

    logger.info("Registering modules into application context")

    loaded = 0

    for name in order:

        module = modules[name]

        if not module.ENABLED:

            logger.info("SKIP  %s (disabled)", module.NAME)
            continue

        register_module(app, module)

        logger.info("OK    %s → registered", module.NAME)

        loaded += 1

    # ============================================================
    section("FINAL STATUS")
    # ============================================================

    logger.info("Framework ready (%s modules loaded successfully)", loaded)

    logger.info("=" * 60)

    return modules