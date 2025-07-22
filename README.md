# virtual-uv

A wrapper that makes [`uv`](https://github.com/astral-sh/uv) use your existing virtual environments instead of creating new ones. It automatically detects your active environment and makes `uv` use it.

## The Problem: `uv` Has the Features, But They're Inconvenient

`uv` does support using existing environments with `UV_PROJECT_ENVIRONMENT` and `--active`, but requires manual setup every time:

```sh
# What uv expects you to do
conda activate my-env
UV_PROJECT_ENVIRONMENT=$CONDA_PREFIX uv add requests  # Manual env var
# or
uv add requests --active  # Remember the flag every time
```

This manual approach is inconvenient for two opposite types of users:

**Power Developers**: You want full control over environments but don't want to babysit `uv` with environment variables and flags every single command.

**ML Researchers**: You just want packages installed in your active environment without thinking about `uv`'s environment management at all. Of course `uv pip` is excellent interface replacing `pip` but it is not project managing feature modifying `pyproject.toml`.

## How Other Tools Handle This

**Poetry does it right**: Poetry respects your active environment and doesn't forcefully manage environments. It also protects conda's base environment by default.

```sh
conda activate my-env
poetry add requests  # Just works, uses your environment
```

**`uv` forces environment decisions**: Even when you have an environment activated, `uv` creates its own unless you manually configure it.

## The Solution: Clean Separation Like Poetry

`virtual-uv` solves this by separating `uv`'s "package management" from "virtual environment management" - giving you poetry's clean workflow with `uv`'s speed.

```sh
pip install virtual-uv

# Now it just works like poetry
conda activate my-env    # You manage environments
vuv add requests         # uv manages packages, automatically uses your env
```

**For Power Developers**: You get full environment control without babysitting `uv` with flags and environment variables.

**For ML Researchers**: You get zero-config package management that respects your carefully crafted environments.

Both get the same thing: clean separation of concerns.


## Demo: The Difference

### Before (Inconvenient)
```sh
# Power developer workflow - manual every time
conda activate my-env
UV_PROJECT_ENVIRONMENT=$CONDA_PREFIX uv add requests
UV_PROJECT_ENVIRONMENT=$CONDA_PREFIX uv add pandas
UV_PROJECT_ENVIRONMENT=$CONDA_PREFIX uv install

# ML researcher workflow - unexpected behavior
conda activate my-research-env  # 50GB with CUDA
uv add transformers             # Creates NEW environment, ignores yours
```

### After (Clean)
```sh
# Both workflows become the same
conda activate my-env           # You manage environment
vuv add requests pandas         # uv manages packages in YOUR environment
vuv install                     # Just works
vuv run python script.py       # Runs in YOUR environment

# Works with any environment manager
python3 -m venv my-env && source my-env/bin/activate
vuv add flask                   # Uses your venv

poetry shell
vuv add django                  # Uses poetry's environment
```

## Usage

```sh
pip install virtual-uv

# Use vuv exactly like uv, but it respects your environment
vuv add package-name
vuv install
vuv run python script.py
vuv <any-uv-command> [arguments]

# For Docker/CI (allow base environment modifications)
VUV_ALLOW_BASE=1 vuv add package-name
```

## How It Works

1. Detects your active virtual environment (conda, virtualenv, etc.)
2. Sets `UV_PROJECT_ENVIRONMENT` to point to your current environment
3. Runs `uv` with the modified environment

```python
# Simplified implementation
if "CONDA_DEFAULT_ENV" in os.environ:
    env["UV_PROJECT_ENVIRONMENT"] = os.environ["CONDA_PREFIX"]
elif "VIRTUAL_ENV" in os.environ:
    env["UV_PROJECT_ENVIRONMENT"] = os.environ["VIRTUAL_ENV"]

subprocess.run(["uv"] + args, env=env)
```

## Requirements

- Python 3.7+
- `uv` installed
- An active virtual environment

## Related Issues

This addresses long-standing `uv` issues:
- [#1703](https://github.com/astral-sh/uv/issues/1703), [#11152](https://github.com/astral-sh/uv/issues/11152), [#11315](https://github.com/astral-sh/uv/issues/11315), [#11273](https://github.com/astral-sh/uv/issues/11273)

## Contributing

Contributions welcome! Submit issues or pull requests.

## License

MIT License. See [LICENSE](LICENSE) for details.

## Author

Created by [MilkClouds](https://github.com/MilkClouds).
