# openrouter-oai-agentsdk

Use OpenRouter models inside the OpenAI Agents SDK without changing your agent architecture.

This package provides:

- an OpenRouter-backed `ModelProvider`
- a ready-to-use `RunConfig` for `Runner.run(...)` and `Runner.run_streamed(...)`
- environment-based configuration with optional OpenRouter attribution headers

## Install

```bash
uv add openrouter-oai-agentsdk
```

Or:

```bash
pip install openrouter-oai-agentsdk
```

## What problem this solves

The OpenAI Agents SDK expects a model provider. This library plugs OpenRouter in as that provider, so you can keep using:

- `Agent(...)`
- `Runner.run(...)` / `Runner.run_streamed(...)`
- `ModelSettings(...)`

Instead of wiring your own client/provider every time, you create one run config from this package and pass it to `Runner`.

## Quick start (step by step)

1. Create or open your project and install dependencies:

```bash
uv add openai-agents openrouter-oai-agentsdk
```

2. Set your OpenRouter API key:

```bash
export OPENROUTER_API_KEY="sk-or-v1-..."
```

3. Create `main.py`:

```python
import asyncio

from openai.types.responses import ResponseTextDeltaEvent
from openai.types.shared import Reasoning

from agents import Agent, ModelSettings, Runner
from openrouter_oai_agentsdk import create_openrouter_run_config


def agent_settings(*, thinking: bool) -> ModelSettings:
    return ModelSettings(reasoning=None if thinking else Reasoning(effort="none"))


agent = Agent(
    name="Math Tutor",
    instructions=(
        "You provide help with math problems. "
        "Explain your reasoning at each step and include examples."
    ),
    model="z-ai/glm-5",
    model_settings=agent_settings(thinking=False),
)


async def main() -> None:
    result = Runner.run_streamed(
        agent,
        "How to calculate the fall rate for something?",
        run_config=create_openrouter_run_config(),
    )
    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(
            event.data, ResponseTextDeltaEvent
        ):
            print(event.data.delta, end="", flush=True)
    print()


if __name__ == "__main__":
    asyncio.run(main())
```

4. Run it:

```bash
uv run python main.py
```

How this works:

- `create_openrouter_run_config()` reads environment variables and returns a `RunConfig`.
- `Runner.run_streamed(..., run_config=...)` uses OpenRouter through that provider.
- `Agent(model="z-ai/glm-5")` picks the specific model for this run.

## Usage patterns

### Pattern A: zero-config run config from env

```python
from openrouter_oai_agentsdk import OPENROUTER_RUN_CONFIG
from agents import Runner

# Pass OPENROUTER_RUN_CONFIG directly to Runner calls.
```

### Pattern B: explicit settings in code

```python
from openrouter_oai_agentsdk import OpenRouterSettings, create_openrouter_run_config

settings = OpenRouterSettings(
    api_key="sk-or-v1-...",
    fallback_model="openai/gpt-5-mini",
    http_referer="https://your-app.example",
    x_title="Your App Name",
)
run_config = create_openrouter_run_config(settings=settings)
```

Use this pattern when you want fully explicit config (service containers, tests, multi-tenant apps).

## Environment variables

Required:

- `OPENROUTER_API_KEY`: your OpenRouter key (`sk-or-v1-...`)

Optional:

- `OPENROUTER_MODEL`: fallback model if an agent does not define one
- `OPENROUTER_BASE_URL`: defaults to `https://openrouter.ai/api/v1`
- `OPENROUTER_HTTP_REFERER`: app/site URL for OpenRouter attribution
- `OPENROUTER_X_TITLE`: app title for OpenRouter attribution
- `OPENROUTER_DISABLE_TRACING`: `true` by default

## Common errors

- `OPENROUTER_API_KEY is not set`: export `OPENROUTER_API_KEY` before running.
- `No model provided`: set `Agent(model=...)` or set `OPENROUTER_MODEL`.

## Import compatibility

The preferred import is:

```python
from openrouter_oai_agentsdk import OPENROUTER_RUN_CONFIG
```

Legacy import path is still supported:

```python
from openrouter_provider import OPENROUTER_RUN_CONFIG
```

## Build and publish (maintainers)

Build distributions:

```bash
uv build --no-sources
```

Bump version:

```bash
uv version --bump patch
```

Publish to PyPI:

```bash
uv publish --token "$UV_PUBLISH_TOKEN"
```

Publish to a configured custom index:

```bash
uv publish --index testpypi --token "$UV_PUBLISH_TOKEN"
```

Trusted publishing from GitHub Actions is also supported via `.github/workflows/publish.yml`.

Verify install/import (without local project shadowing):

```bash
uv run --with openrouter-oai-agentsdk --no-project -- \
  python -c "import openrouter_oai_agentsdk; print(openrouter_oai_agentsdk.__version__)"
```
