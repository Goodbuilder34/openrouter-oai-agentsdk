"""Public package exports for openrouter-oai-agentsdk."""

from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version

from .provider import (
    DEFAULT_OPENROUTER_BASE_URL,
    OPENROUTER_RUN_CONFIG,
    OpenRouterModelProvider,
    OpenRouterSettings,
    create_openrouter_client,
    create_openrouter_run_config,
)

try:
    __version__ = version("openrouter-oai-agentsdk")
except PackageNotFoundError:
    __version__ = "0.0.0"

__all__ = [
    "DEFAULT_OPENROUTER_BASE_URL",
    "OPENROUTER_RUN_CONFIG",
    "OpenRouterModelProvider",
    "OpenRouterSettings",
    "create_openrouter_client",
    "create_openrouter_run_config",
    "__version__",
]
