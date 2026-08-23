"""Load Monobank modules without importing Home Assistant lifecycle code."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import sys
from types import ModuleType


ROOT = Path(__file__).resolve().parents[1]
COMPONENT_DIR = ROOT / "custom_components" / "monobank"


def load_monobank_module(name: str) -> ModuleType:
    """Load one integration module in a lightweight package namespace."""
    if name == "api" and "aiohttp" not in sys.modules:
        try:
            __import__("aiohttp")
        except ModuleNotFoundError:
            aiohttp = ModuleType("aiohttp")

            class ClientError(Exception):
                """Minimal aiohttp client error stand-in."""

            class ClientSession:
                """Minimal aiohttp client session stand-in."""

            aiohttp.ClientError = ClientError
            aiohttp.ClientSession = ClientSession
            aiohttp.ClientResponse = object
            sys.modules["aiohttp"] = aiohttp

    custom_components = sys.modules.setdefault(
        "custom_components", ModuleType("custom_components")
    )
    custom_components.__path__ = [str(ROOT / "custom_components")]

    package = sys.modules.setdefault(
        "custom_components.monobank", ModuleType("custom_components.monobank")
    )
    package.__path__ = [str(COMPONENT_DIR)]

    module_name = f"custom_components.monobank.{name}"
    if module_name in sys.modules:
        return sys.modules[module_name]

    spec = importlib.util.spec_from_file_location(
        module_name, COMPONENT_DIR / f"{name}.py"
    )
    if spec is None or spec.loader is None:
        raise ImportError(f"Unable to load {module_name}")

    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module
