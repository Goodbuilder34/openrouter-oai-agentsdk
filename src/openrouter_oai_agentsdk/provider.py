"""OpenRouter model provider integration for the OpenAI Agents SDK."""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Final

from agents import (
    Model,
    ModelProvider,
    OpenAIChatCompletionsModel,
    RunConfig,
    set_tracing_disabled,
)
from openai import AsyncOpenAI

DEFAULT_OPENROUTER_BASE_URL: Final[str] = "https://openrouter.ai/api/v1"
_MISSING_API_KEY_SENTINEL: Final[str] = "missing-openrouter-api-key"


def _strip_or_none(value: str | None) -> str | None:
    if value is None:
        return None
    stripped = value.strip()
    return stripped or None


def _get_bool_env(name: str, *, default: bool) -> bool:
    raw_value = _strip_or_none(os.getenv(name))
    if raw_value is None:
        return default
    return raw_value.lower() not in {"0", "false", "no", "off"}


@dataclass(frozen=True, slots=True)
class OpenRouterSettings:
    """Configuration used to create OpenRouter-backed Agents SDK clients."""

    api_key: str | None
    fallback_model: str | None = None
    base_url: str = DEFAULT_OPENROUTER_BASE_URL
    http_referer: str | None = None
    x_title: str | None = None
    disable_tracing: bool = True

    @classmethod
    def from_env(cls) -> OpenRouterSettings:
        return cls(
            api_key=_strip_or_none(os.getenv("OPENROUTER_API_KEY")),
            fallback_model=_strip_or_none(os.getenv("OPENROUTER_MODEL")),
            base_url=_strip_or_none(os.getenv("OPENROUTER_BASE_URL"))
            or DEFAULT_OPENROUTER_BASE_URL,
            http_referer=_strip_or_none(os.getenv("OPENROUTER_HTTP_REFERER")),
            x_title=_strip_or_none(os.getenv("OPENROUTER_X_TITLE")),
            disable_tracing=_get_bool_env(
                "OPENROUTER_DISABLE_TRACING",
                default=True,
            ),
        )

    @property
    def default_headers(self) -> dict[str, str] | None:
        headers: dict[str, str] = {}
        if self.http_referer:
            headers["HTTP-Referer"] = self.http_referer
        if self.x_title:
            headers["X-Title"] = self.x_title
        return headers or None

    def ensure_api_key(self) -> None:
        if self.api_key:
            return
        raise ValueError(
            "OPENROUTER_API_KEY is not set. Export it before running, for example:\n"
            "export OPENROUTER_API_KEY='sk-or-v1-...'"
        )


def create_openrouter_client(
    settings: OpenRouterSettings | None = None,
) -> AsyncOpenAI:
    """Build an AsyncOpenAI client configured for OpenRouter."""

    resolved = settings or OpenRouterSettings.from_env()
    return AsyncOpenAI(
        base_url=resolved.base_url,
        api_key=resolved.api_key or _MISSING_API_KEY_SENTINEL,
        default_headers=resolved.default_headers,
    )


class OpenRouterModelProvider(ModelProvider):
    """Model provider that routes model calls to OpenRouter."""

    def __init__(
        self,
        *,
        settings: OpenRouterSettings | None = None,
        client: AsyncOpenAI | None = None,
        fallback_model: str | None = None,
    ) -> None:
        self._settings = settings or OpenRouterSettings.from_env()
        self._client = client or create_openrouter_client(self._settings)
        self._fallback_model = (
            fallback_model if fallback_model is not None else self._settings.fallback_model
        )

    def get_model(self, model_name: str | None) -> Model:
        self._settings.ensure_api_key()

        selected_model = model_name or self._fallback_model
        if not selected_model:
            raise ValueError(
                "No model provided. Set Agent(model=...) or OPENROUTER_MODEL."
            )

        return OpenAIChatCompletionsModel(
            model=selected_model,
            openai_client=self._client,
        )


def create_openrouter_run_config(
    *,
    settings: OpenRouterSettings | None = None,
    client: AsyncOpenAI | None = None,
    fallback_model: str | None = None,
    disable_tracing: bool | None = None,
) -> RunConfig:
    """Create a RunConfig using the OpenRouter model provider."""

    resolved_settings = settings or OpenRouterSettings.from_env()
    should_disable_tracing = (
        resolved_settings.disable_tracing
        if disable_tracing is None
        else disable_tracing
    )
    if should_disable_tracing:
        set_tracing_disabled(disabled=True)

    provider = OpenRouterModelProvider(
        settings=resolved_settings,
        client=client,
        fallback_model=fallback_model,
    )
    return RunConfig(model_provider=provider)


OPENROUTER_RUN_CONFIG = create_openrouter_run_config()
