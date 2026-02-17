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
from agents import Agent, Runner
from openrouter_oai_agentsdk import create_openrouter_run_config

agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant.",
    model="openai/gpt-4o-mini",
)

result = Runner.run_sync(
    agent,
    "In one sentence, what is gravity?",
    run_config=create_openrouter_run_config(),
)
print(result.final_output)
```

4. Run it:

```bash
uv run python main.py
```

What each line does:

1. `Agent(...)` defines behavior and the model you want.
2. `create_openrouter_run_config()` wires OpenRouter as the provider.
3. `Runner.run_sync(...)` executes one request using that provider.
4. `result.final_output` prints the agent's final text response.

If you already set `OPENROUTER_MODEL`, you can omit `model=...` on `Agent(...)`.

## Next step: streaming (optional)

Use `Runner.run_streamed(...)` only when you want token-by-token output in real time. Start with `run_sync` first.

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
