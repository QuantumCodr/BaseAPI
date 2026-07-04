"""
Plugin Registry

Future plugin discovery starts here.
"""

PLUGINS = {}


def register_plugin(name: str, plugin):
    PLUGINS[name] = plugin


def get_plugin(name: str):
    return PLUGINS.get(name)


def list_plugins():
    return sorted(PLUGINS.keys())