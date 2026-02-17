"""CLI entry points for quick local verification."""

from __future__ import annotations

from .provider import OpenRouterSettings, create_openrouter_run_config


def main() -> None:
    settings = OpenRouterSettings.from_env()
    if not settings.api_key:
        raise SystemExit(
            "OPENROUTER_API_KEY is not set. Export it and run this command again."
        )
    create_openrouter_run_config(settings=settings)
    print("OpenRouter run config initialized successfully.")


if __name__ == "__main__":
    main()
