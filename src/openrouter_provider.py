"""Backward-compatible import path for older integrations."""

from openrouter_oai_agentsdk import (
    DEFAULT_OPENROUTER_BASE_URL,
    OPENROUTER_RUN_CONFIG,
    OpenRouterModelProvider,
    OpenRouterSettings,
    create_openrouter_client,
    create_openrouter_run_config,
)

__all__ = [
    "DEFAULT_OPENROUTER_BASE_URL",
    "OPENROUTER_RUN_CONFIG",
    "OpenRouterModelProvider",
    "OpenRouterSettings",
    "create_openrouter_client",
    "create_openrouter_run_config",
]
