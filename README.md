# virtual-uv

Makes [`uv`](https://github.com/astral-sh/uv) respect your existing virtual environments instead of creating new ones. Protects conda base environment by default.

```sh
pip install virtual-uv

# Works with any environment
conda activate my-env                              # conda
# python3 -m venv my-env && . my-env/bin/activate  # venv
# uv venv my-env && . my-env/bin/activate          # uv venv

vuv add requests pandas         # Uses YOUR environment (not a new one)
vuv install                     # As `poetry install`, install project without removing existing packages

# All uv commands work
vuv <any-uv-command> [arguments]

# For CI/CD or Docker (allow base environment modifications)
VUV_ALLOW_BASE=1 vuv add package-name
# Or use uv's system Python feature: UV_SYSTEM_PYTHON=1 vuv add package-name
```

**Real-world example**: See virtual-uv in action in [this GitHub Actions workflow](https://github.com/open-world-agents/open-world-agents/blob/main/.github/workflows/ci.yml) using conda + vuv for CI/CD.

## Why You Need This

`uv` has `UV_PROJECT_ENVIRONMENT` and `--active` but you have to configure them:

```sh
# What uv makes you do
export UV_PROJECT_ENVIRONMENT=$CONDA_PREFIX  # Set up once per project/shell
# or add to .bashrc, or use --active flag, or set in .envvl...
uv add requests  # Now it works, but you had to think about it
```

`virtual-uv` automates this completely - zero configuration:

```sh
# What vuv lets you do
conda activate my-env
vuv add requests  # Just works, no setup needed
```

**The key difference**: You shouldn't have to think about environment configuration at all.

> **Why not per-project virtual environments? It's better practice.**  
> Yes, it's controversial part, I know. But ML researchers commonly face the situation which installs tons of GB size packages (like PyTorch, TensorFlow, etc.) and it's not feasible to create a new environment for each project especially for brainstorming and prototyping. The fact that researchers does NOT commonly need strict dependency management is also a reason. (Most researchers get satisfied with single requirements.txt haha)

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
