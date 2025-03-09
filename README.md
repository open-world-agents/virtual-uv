# vuv

A wrapper script for [`uv`](https://github.com/astral-sh/uv) enabling automatic virtual environment detection and configuration.

## Motivation

`uv`, by defaults without [`UV_PROJECT_ENVIRONMENT` customization](https://docs.astral.sh/uv/configuration/environment/#uv_project_environment), **forcefully creates and activates its own virtual environment, even when you already have one activated.** This behavior can be inconvenient, *especially when working in a monorepo setup.*

In monorepo development, `uv` only supports:

1. Using a single environment across all sub-repositories, or
2. Using separate environments for each sub-repository.

However, these options lack flexibility. They do not allow you to *selectively install and manage dependencies across some sub-repositories with flexible interdependencies.*

The existing virtual environment support in `uv` is limited and doesn't accommodate such scenarios. It provides only minimal customization through environment variables.

To address these limitations, **`vuv`** was created. It allows `uv` to detect and use your currently activated virtual environment, providing the flexibility needed for complex project structures without forcing the creation of new environments.

Related issues in `uv`: https://github.com/astral-sh/uv/issues/1703, https://github.com/astral-sh/uv/issues/11152, https://github.com/astral-sh/uv/issues/11315, https://github.com/astral-sh/uv/issues/11273, ...

If equivalent feature is implemented in `uv`, this repo would be useless; I hope that time comes soon, since I'm waiting over 1 year.


## Features

- **Respects Existing Virtual Environments**: If a virtual environment is already activated (managed by `conda`, `virtualenv`, etc.), `vuv` ensures that `uv` uses it instead of creating a new one.

- **Seamless Integration with `uv`**: Use `vuv` just like `uv`; all commands and arguments are passed directly to `uv`.

- **`vuv install`**: `uv`, by defaults, forcefully sync whole project dependencies into python environment and it leads possible environment corruption when we use pre-existing environments. To support `install` instead of `sync` and to match `uv` behavior with `poetry`, we supports `vuv install` commands. It's implemented as simple; just it remaps `vuv install` into `uv sync --inexact`.

## Installation

```sh
pip install virtual-uv
```

## Usage

Use `vuv` as a drop-in replacement for `uv`.

### Examples

```sh
# Add a package to your project
vuv add package-name

# Install dependencies (equivalent to 'uv sync --inexact')
vuv install

# Run other uv commands
vuv <uv-command> [arguments]
```

### Note

- **Virtual Environment Required**: `vuv` requires an active virtual environment. If none is detected, to prevent unexpected behavior, it will prompt you to activate one. If you require system-wide install, use pure `uv` instead of `vuv`.
- **`conda`'s `base` environment is protected**: By defaults, `vuv` prevents users to modify package in `base` environment in `conda`.

## How It Works

When you run a command with `vuv`:

1. **Checks for an Active Virtual Environment**:
   - For **conda**, it checks if `CONDA_DEFAULT_ENV` is set and not equal to `base`.
   - For **virtualenv**, it checks if `VIRTUAL_ENV` is set.
2. **Sets Environment Variables**:
   - Sets `UV_PROJECT_ENVIRONMENT` to point to your current virtual environment, so `uv` uses it instead of creating a new one.
3. **Runs the `uv` Command**:
   - Passes all arguments to `uv` with the modified environment variables.

## Requirements

- **Python**: 3.7 or higher
- **uv**: Ensure `uv` is installed and accessible from the command line.
- **Virtual Environment**: An active virtual environment managed by `conda`, `virtualenv`, or similar tools.

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

## License

This project is licensed under the MIT License.

## Author

Developed by [MilkClouds](mailto:milkclouds00@gmail.com).