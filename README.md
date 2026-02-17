# openrouter-oai-agentsdk

OpenRouter provider utilities for the OpenAI Agents SDK.

## Install

```bash
uv add openrouter-oai-agentsdk
```

Or:

```bash
pip install openrouter-oai-agentsdk
```

## Environment variables

Required:

- `OPENROUTER_API_KEY`: your OpenRouter key (`sk-or-v1-...`)

Optional:

- `OPENROUTER_MODEL`: fallback model if an agent does not define one
- `OPENROUTER_BASE_URL`: defaults to `https://openrouter.ai/api/v1`
- `OPENROUTER_HTTP_REFERER`: app/site URL for OpenRouter attribution
- `OPENROUTER_X_TITLE`: app title for OpenRouter attribution
- `OPENROUTER_DISABLE_TRACING`: `true` by default

## Quick start

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

## Import compatibility

The preferred import is:

```python
from openrouter_oai_agentsdk import OPENROUTER_RUN_CONFIG
```

Legacy import path is still supported:

```python
from openrouter_provider import OPENROUTER_RUN_CONFIG
```

## Build and publish with `uv`

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

Verify install/import (without local project shadowing):

```bash
uv run --with openrouter-oai-agentsdk --no-project -- \
  python -c "import openrouter_oai_agentsdk; print(openrouter_oai_agentsdk.__version__)"
```
