# **UV Python Packages and Project Manager**

## **What Is uv**

uv is a Python package and project manager built by Astral, the same team behind the Ruff linter, written in Rust for speed. It is designed to replace a whole pile of separate tools that Python developers have traditionally had to juggle: `pip` for installing packages, `venv` for virtual environments, `pyenv` for managing multiple Python versions, `pip-tools` or `poetry` for locking dependencies, `pipx` for running command-line tools without polluting a project's environment, and `twine` for publishing. uv folds all of that into one binary.

The main reasons people adopt it are:

- **Speed.** Dependency resolution and installs are often 10 to 100 times faster than pip. A cold `uvx ruff --version` takes around a second; a cached run is in the tens of milliseconds.
- **One tool, one workflow.** The same commands work for a quick script, a multi-package monorepo, a Docker image, and a CI pipeline.
- **A lockfile by default.** `uv.lock` captures the exact resolved versions, including cross-platform markers, so every teammate and CI runner installs the same thing.
- **Built-in Python management.** No need to install `pyenv` or rely on whatever Python the system has — uv can download and pin a specific interpreter per project.
- **No Python required to run uv itself.** The binary is a self-contained Rust executable, so a brand-new machine can `curl | sh` uv and immediately manage Python.

### **Installing uv**

```bash
# macOS / Linux (official installer)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows PowerShell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# Through pip, if you already have Python (slower, but works)
pip install uv

# Through Homebrew on macOS
brew install uv

# Verify
uv --version

# Keep uv itself up to date
uv self update
```

After the official installer, the `uv` binary is placed in `~/.cargo/bin` on Linux/macOS or `%USERPROFILE%\.cargo\bin` on Windows, and the path is added to your shell profile.

## **The Core Idea: Project-Centric Workflow**

Traditionally, working on a Python project meant a sequence like: create a venv, activate it, `pip install` things one by one, remember to update `requirements.txt`, and hope everyone on the team has the same versions installed. uv replaces this with a small, repeatable loop centered on `pyproject.toml` and `uv.lock`, and it manages the virtual environment automatically behind the scenes, so there is no separate manual "activate" step needed for day-to-day commands.

The two main files:

- `pyproject.toml` — what the project is willing to accept (loose constraints, project metadata, scripts).
- `uv.lock` — what was actually resolved and installed (exact versions, hashes, platform markers). This is the file that should be committed to git for applications.

### **Starting a New Project**

```bash
uv init myproject
cd myproject
```

`uv init` creates a `pyproject.toml`, a starter `main.py`, a `README.md`, a `.gitignore`, and a `.python-version` file. Running any `uv` command afterward, like `uv run`, will automatically create a `.venv` folder and a `uv.lock` file the first time it is needed.

```bash
uv run main.py
```

Output:

```
Using CPython 3.13.2
Creating virtual environment at: .venv
Hello from myproject!
```

Walking through this: `uv run` checks whether the environment matches `pyproject.toml` and `uv.lock`, creates or updates the virtual environment if needed, and then runs the given command inside it — all without the developer ever typing `source .venv/bin/activate`.

### **Resulting Project Layout**

```
myproject/
    pyproject.toml     # project metadata and dependencies, commit this
    uv.lock             # exact locked versions, commit this for apps
    .python-version     # pinned Python version, commit this
    .gitignore          # should include .venv/
    .venv/               # the virtual environment itself, do not commit
    main.py
    README.md
```

## **Managing Dependencies**

### **Adding a Package**

```bash
uv add requests
```

This does three things at once: installs `requests` into `.venv`, adds it under `[project].dependencies` in `pyproject.toml`, and updates `uv.lock` with the exact resolved version.

```toml
[project]
name = "myproject"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = [
    "requests>=2.32.0",
]
```

Adding multiple packages, or pinning an exact version, works the same way:

```bash
uv add fastapi uvicorn
uv add "pandas==2.2.3"
uv add "django>=4.2,<5.0"
```

### **Adding Development-Only Dependencies**

Tools like test runners and linters should not be installed for people who only use the package; they belong in a separate dev group:

```bash
uv add --dev pytest ruff mypy
```

This is written into `pyproject.toml` under `[dependency-groups]`:

```toml
[dependency-groups]
dev = [
    "pytest>=8.0",
    "ruff>=0.6",
    "mypy>=1.10",
]
```

Multiple groups are allowed. A common split is `dev` for general development and `docs` for documentation-only tools:

```bash
uv add --group docs sphinx sphinx-rtd-theme myst-parser
```

```toml
[dependency-groups]
dev  = ["pytest>=8.0", "ruff>=0.6"]
docs = ["sphinx>=7.0", "sphinx-rtd-theme>=2.0", "myst-parser>=3.0"]
```

Install only what is needed for a task:

```bash
uv sync --no-dev                  # production: no dev tools
uv sync --group docs              # include docs group
uv sync --all-groups              # everything
```

### **Optional Dependencies and Extras**

These are the dependencies that should be available to users of the library but not pulled in by default:

```bash
uv add --optional requests httpx
```

This adds an `http` extra to `pyproject.toml`:

```toml
[project.optional-dependencies]
http = ["requests>=2.32", "httpx>=0.27"]
```

Users can then install with the extra:

```
pip install myproject[http]
uv sync --extra http
uv sync --all-extras
```

The difference between `[project.optional-dependencies]` and `[dependency-groups]`:

- **Extras** are part of the package's published metadata. They are intended for end users of the library.
- **Groups** are for the maintainers. They are not installed when someone installs the package from PyPI; they are only used inside the project itself.

### **Removing a Package**

```bash
uv remove requests
```

This removes it from both `pyproject.toml` and `uv.lock`, and updates the environment to match.

### **Installing Everything From the Lockfile**

```bash
uv sync
```

`uv sync` is the command a teammate runs after cloning the repository, or after pulling changes. It reads `pyproject.toml` and `uv.lock`, creates or updates `.venv` to match exactly, and installs everything needed in one step, without manually creating a venv or running `pip install` in a loop.

```bash
uv sync --frozen --no-dev
```

`--frozen` tells uv to trust `uv.lock` exactly as it is, without re-resolving anything, which is useful in CI/CD for speed and determinism. `--no-dev` skips the dev dependency group, which is typical for a production deployment that does not need test tools.

Other useful flags:

- `uv sync --inexact` — install required packages but do not remove extraneous ones already in the environment.
- `uv sync --no-install-project` — install dependencies but not the project itself (useful for faster test setup).
- `uv sync --extra <name>` — include a specific optional extra.
- `uv sync --all-packages` — install all workspace members.

### **Locking Without Installing**

```bash
uv lock                              # refresh uv.lock from pyproject.toml
uv lock --upgrade                    # upgrade everything to the latest allowed versions
uv lock --upgrade-package fastapi     # upgrade just one package
uv lock --upgrade-package fastapi==0.115.0  # upgrade to a specific version
uv lock --check                      # exit non-zero if pyproject.toml and uv.lock disagree
uv lock --locked                     # refuse to run if uv.lock is out of date
```

### **Inspecting Dependencies**

```bash
uv tree
```

This prints the full dependency tree, which is useful for spotting where a conflicting or unexpectedly heavy package is being pulled in from. You can scope it:

```bash
uv tree --package requests           # only show what depends on requests
uv tree --depth 2                    # limit depth
uv tree --invert                     # reverse tree: who depends on this package
```

## **`pyproject.toml` Instead of `requirements.txt`**

### **Why the Switch**

`requirements.txt` is just a flat list of package names, sometimes with pinned versions, with no distinction between what the actual application needs versus what is only needed for development, no built-in place for project metadata, and no separate concept of "the versions I want" versus "the versions that were actually resolved and installed." `pyproject.toml` plus `uv.lock` splits those two concerns cleanly: `pyproject.toml` holds loose constraints (what you are willing to accept), and `uv.lock` holds the exact resolved versions (what was actually installed), which is what makes builds reproducible across different machines and CI runners.

| Aspect | requirements.txt | pyproject.toml + uv.lock |
|---|---|---|
| Project metadata (name, version) | Not supported | Supported under `[project]` |
| Separates prod vs dev dependencies | Needs separate files, e.g. `requirements-dev.txt` | Built in via `[dependency-groups]` |
| Exact reproducible versions | Only if every version is manually pinned | Automatic, in `uv.lock` |
| Cross-platform lock (Windows/Linux/Mac differences) | Not represented | Supported natively |
| Standardized by Python packaging (PEP 621) | No | Yes |
| Holds hashes for security audits | Possible with `pip-compile` | Yes, built into `uv.lock` |

### **Migrating an Existing requirements.txt Project**

```bash
# 1. Create a minimal pyproject.toml (skip this if one already exists)
uv init --bare

# 2. Import all dependencies from the old file
uv add -r requirements.txt

# 3. Import dev-only dependencies into the dev group
uv add --dev -r requirements-dev.txt
```

`uv add -r requirements.txt` reads every line of the old file and writes each package into `[project].dependencies`. If the old file had a pin like `requests==2.31.0`, uv typically adds just `requests` as the constraint and lets `uv.lock` capture the exact resolved version instead, since hard pins in `pyproject.toml` are usually looser than what a lockfile should hold. If keeping an exact hard pin in `pyproject.toml` itself is important — for example a package known to break on newer releases — it can be passed explicitly:

```bash
uv add "requests==2.31.0"
```

If `requirements-dev.txt` includes the base file with `-r requirements.txt` inside it, that reference line should be stripped first so the base dependencies are not accidentally duplicated into the dev group:

```bash
sed '/^-r /d' requirements-dev.txt > requirements-dev-only.txt
uv add --dev -r requirements-dev-only.txt
```

After migration, `requirements.txt` can be deleted (or kept temporarily as a reference) once the team has verified `uv sync` reproduces a working environment.

### **Exporting Back to `requirements.txt` (If Something Else Still Needs It)**

If a downstream tool — a legacy CI script, a container image, an internal artifact system — strictly requires a `requirements.txt` file, it can be regenerated on the fly without maintaining it by hand:

```bash
uv export --format requirements-txt -o requirements.txt
uv export --format requirements-txt --no-hashes          # drop the hashes line
uv export --format requirements-txt --no-dev             # skip dev group
uv export --format pylock.toml                            # PEP 751
uv export --format cyclonedx1.5                           # CycloneDX SBOM for security audits
```

This means `requirements.txt` becomes a generated artifact, not a hand-edited source of truth.

## **The pip-Compatible Interface (`uv pip`)**

For situations where the full project workflow is not wanted — a quick one-off script, an existing CI pipeline, or a Dockerfile that already expects pip-style commands — uv ships a drop-in pip-compatible layer under `uv pip`:

```bash
uv pip install requests
uv pip install -r requirements.txt
uv pip uninstall requests
uv pip list
uv pip freeze > requirements.txt
uv pip compile requirements.in -o requirements.txt
uv pip sync requirements.txt
```

These commands behave like their `pip` equivalents but run through uv's much faster resolver and installer. The same module is also how you can produce a `requirements.txt` from a more complex `pyproject.toml` if a downstream system needs it.

This is the recommended path for legacy projects with heavy custom pip tooling, corporate environments with locked-down processes, or very old Python versions, without needing to restructure the whole project around `pyproject.toml` right away.

### **`uv pip compile` — Locking Without uv Projects**

`uv pip compile` is uv's answer to `pip-compile` from `pip-tools`. It takes a loose `requirements.in` file and produces a fully resolved `requirements.txt` with hashes:

```bash
uv pip compile requirements.in -o requirements.txt
```

Useful flags:

```bash
uv pip compile requirements.in --upgrade                  # upgrade everything
uv pip compile requirements.in --upgrade-package requests  # upgrade just one
uv pip compile requirements.in --universal                 # output one file for both py2/py3
uv pip compile requirements.in --python-version 3.12       # pin the target Python
```

## **Managing Python Versions**

uv can download and manage Python interpreters directly, replacing the need for a separate tool like `pyenv`.

```bash
uv python install 3.12 3.13      # install one or more Python versions
uv python list                    # show installed and available versions
uv python list --only-installed    # only what is already on the machine
uv python find 3.12               # print the path to a specific interpreter
uv python pin 3.12                # write .python-version, pinning this project
uv python uninstall 3.11          # remove an installed interpreter
```

`uv python pin` writes a `.python-version` file, which other uv commands then respect automatically. If `pyproject.toml` declares `requires-python = ">=3.10"`, any pinned version that satisfies that constraint can be swapped in later, and running `uv sync` afterward rebuilds `.venv` against the newly pinned interpreter.

uv also ships its own `python` shim. If `uv` is on `PATH` and a project has a `.python-version` file, running plain `python` (or `python3`) at the project root will use the pinned interpreter:

```bash
uv python install                 # installs the version from .python-version
python --version                  # uses it
```

## **Running Standalone Tools With `uvx` and `uv tool`**

There are three ways to run a Python command-line tool, and the choice depends on whether the tool is a one-off, persistent, or part of a project.

### **`uvx` (alias for `uv tool run`) — Ephemeral**

`uvx` is uv's equivalent of Node's `npx`. It runs a command from a Python package in a temporary, isolated environment, without installing that package globally or adding it to the current project.

```bash
uvx ruff check .
uvx black --check .
uvx cowsay "hello from uv"
uvx pycowsay 'hello world!'
```

A cached run is in the tens of milliseconds. The tool is installed once into uv's cache, then run on demand, and not added to your project.

### **`uv tool install` — Persistent**

If a tool is used often, install it once so it lives on `PATH`:

```bash
uv tool install ruff
uv tool install black
uv tool list                     # show all installed tools
uv tool uninstall ruff
uv tool update --all             # upgrade every installed tool
```

This is uv's replacement for `pipx`. The installed command is placed in `~/.local/bin` on Linux/macOS, or `%USERPROFILE%\.local\bin` on Windows, and added to `PATH` automatically by the installer.

### **`uv run` — Inside a Project**

When the tool needs to see your project's own dependencies (for example, running `pytest` against the code in your project, or `flask run` with a project-local Flask app), use `uv run` instead of `uvx`:

```bash
uv run pytest
uv run flask --app myapp run
uv run python my_script.py
```

### **Which One to Use — Quick Decision**

| Situation | Use |
|---|---|
| One-off inspection of a file or directory | `uvx` |
| Tool used daily, on many projects | `uv tool install` |
| Tool needs to import the project itself (tests, type checks) | `uv run` |

## **Workspaces — Multi-Package Projects**

For larger codebases that should be split into multiple packages but still share a single lockfile, uv supports Cargo-style workspaces. A workspace is "a collection of one or more packages, called workspace members, that are managed together."

```
monorepo/
├── pyproject.toml          # workspace root
├── uv.lock                  # single shared lockfile
├── core/
│   └── pyproject.toml      # workspace member
└── web/
    └── pyproject.toml      # workspace member
```

The root `pyproject.toml` declares the workspace:

```toml
[project]
name = "monorepo"
version = "0.1.0"
requires-python = ">=3.11"

[tool.uv.workspace]
members = ["core", "web"]
exclude = ["legacy-*"]
```

`core/pyproject.toml` can then depend on the local `web` package through `tool.uv.sources`:

```toml
[project]
name = "core"
dependencies = ["web"]

[tool.uv.sources]
web = { workspace = true }
```

Walking through the design:

- One `uv.lock` covers the entire workspace, so versions stay consistent across packages.
- `uv lock` operates on the whole workspace; `uv run` and `uv sync` operate on the root by default but accept `--package <name>` to target a specific member.
- Dependencies between members are declared via `tool.uv.sources` and are resolved to the local source, not to PyPI.
- Members can be applications or libraries.

This is the right structure for any project where "the code" naturally splits into more than one deployable unit.

## **Building, Publishing, and the Project Lifecycle**

uv covers the full packaging workflow, not just install and run.

### **`uv build` — Build Distributions**

```bash
uv build
```

This produces a `dist/` folder with a wheel and an sdist, exactly like `python -m build`. It works with the same `pyproject.toml` and reads the `[build-system]` table to pick a backend.

```bash
uv build --wheel          # only the wheel
uv build --sdist          # only the source distribution
uv build --out-dir out/   # custom output folder
```

### **`uv publish` — Publish to an Index**

```bash
uv publish                          # default: PyPI
uv publish --publish-url https://test.pypi.org/legacy/   # Test PyPI
uv publish --token pypi-...          # API token
```

`uv publish` is uv's replacement for `twine`. It reads the same credentials from `~/.pypirc` or environment variables (`UV_PUBLISH_TOKEN`, `UV_PUBLISH_USERNAME`, `UV_PUBLISH_PASSWORD`).

### **`uv version` — Bump the Project Version**

```bash
uv version                  # show current version
uv version 1.2.0            # set to a specific value
uv version --bump major     # 0.1.0 -> 1.0.0
uv version --bump minor     # 0.1.0 -> 0.2.0
uv version --bump patch     # 0.1.0 -> 0.1.1
uv version --short          # only the number, no "myproject 0.1.0" prefix
```

`uv version` updates the version field in `pyproject.toml`. Use `uv version --bump patch` as the last step before `uv publish` for a quick release.

### **`uv format` — Format Code With Ruff**

uv ships a built-in code formatter that uses Ruff's formatter under the hood:

```bash
uv format              # format all Python files in the project
uv format --check      # exit non-zero if any file would be reformatted
uv format --diff       # show the diff that would be applied
uv format file.py      # format a single file
```

Configuration is read from `[tool.ruff.format]` in `pyproject.toml`, so the same settings are shared with `ruff format` if you have Ruff installed.

### **`uv check` — Type-Check the Project**

Added in uv 0.11.18, this runs the Astral `ty` type checker:

```bash
uv check
```

By default, all Python files in the project are type-checked after the environment is synced.

### **`uv audit` — Check for Known Vulnerabilities**

Added in uv 0.10.12, this checks locked dependencies against the OSV (Open Source Vulnerabilities) database:

```bash
uv audit
```

Exits with a non-zero status if any locked package has a known security advisory. Useful in CI.

## **Locking and Syncing in Detail**

`uv run` automatically re-locks and re-syncs the environment if `pyproject.toml` or `uv.lock` has changed. There are flags to control this:

| Flag | Effect |
|---|---|
| `--frozen` | Use the lockfile as the source of truth, do not re-resolve. Fails if the lockfile is missing. |
| `--locked` | Refuse to run if the lockfile is out of date with `pyproject.toml`. |
| `--no-sync` | Skip environment sync entirely. |
| `--inexact` | Install required packages but do not remove extraneous ones. |
| `--exact` | Remove any package that is not in the lockfile (this is the default for `uv sync`). |
| `--all-packages` | Install all workspace members, not just the root. |

The relationship between `uv lock` and `uv sync`:

- `uv lock` updates `uv.lock` from `pyproject.toml`. It does not install anything.
- `uv sync` updates `.venv` from `pyproject.toml` and `uv.lock`. It does not modify `uv.lock` unless it has to.
- `uv run` does both, on demand, before running the requested command.

## **Environment Variables**

A handful of environment variables change uv's behavior. The most useful:

| Variable | Effect |
|---|---|
| `UV_PYTHON` | Override the Python version for a single command. |
| `UV_PROJECT` | Override the project root path. |
| `UV_INDEX_URL` | Custom package index (replaces PyPI). |
| `UV_EXTRA_INDEX_URL` | Additional package indexes. |
| `UV_FROZEN` | Equivalent to passing `--frozen` to every command. |
| `UV_LOCKED` | Equivalent to passing `--locked` to every command. |
| `UV_NO_CACHE` | Disable the global cache (useful in CI to ensure a clean resolve). |
| `UV_OFFLINE` | Run without network access; resolve only against the local cache. |
| `UV_LINK_MODE=copy` | Use file copying instead of symlinks in the venv (useful on Windows). |
| `UV_PUBLISH_TOKEN` | PyPI token for `uv publish`. |
| `UV_CACHE_DIR` | Override the location of the cache directory. |

Example: building a Docker image with no network and no cache:

```bash
UV_OFFLINE=1 UV_NO_CACHE=1 uv sync --frozen --no-dev
```

## **A Complete Day-to-Day Flow**

```bash
# Starting the day: get the latest dependencies teammates have added
git pull
uv sync

# Working: add something new
uv add scikit-learn

# Running code and tests through the managed environment
uv run python train_model.py
uv run pytest

# Format and lint
uv format
uvx ruff check .

# Committing the change
git add pyproject.toml uv.lock
git commit -m "add scikit-learn for model training"
git push
```

No `pip freeze`, no manually activating a venv, no separately maintained `requirements.txt`. `uv.lock` and `pyproject.toml` together are the single source of truth, and everyone on the team ends up with the exact same resolved versions after `uv sync`.

## **Case Study 1: Migrating a Small FastAPI Service**

Consider a small internal FastAPI service that has been using `pip` and a plain `requirements.txt` for a year, has a separate `requirements-dev.txt` for `pytest` and `ruff`, and is deployed through a Dockerfile that runs `pip install -r requirements.txt`.

**Step 1: Try uv without changing anything yet.**

```bash
uv venv --python 3.12
uv pip install -r requirements.txt
```

This confirms the project still works under uv's pip-compatible layer, with no structural change required, and is a safe first step before committing to the full migration.

**Step 2: Create `pyproject.toml` and import dependencies.**

```bash
uv init --bare
uv add -r requirements.txt
uv add --dev -r requirements-dev.txt
```

**Step 3: Verify the app still runs and tests still pass.**

```bash
uv run uvicorn main:app --reload
uv run pytest
```

**Step 4: Update the Dockerfile.**

```dockerfile
# Before
RUN pip install -r requirements.txt
CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]

# After (multi-stage, fully reproducible)
FROM python:3.12-slim AS builder
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

FROM python:3.12-slim
COPY --from=builder /app/.venv /app/.venv
COPY ./src /app/src
WORKDIR /app
ENV PATH="/app/.venv/bin:$PATH"
CMD ["uvicorn", "myapp.main:app", "--host", "0.0.0.0"]
```

The build stage uses the official uv container image, syncs from the lockfile only, and produces a clean `.venv` that the runtime stage copies in. The runtime stage is just the slim Python image with the prebuilt environment — no pip or uv needed at runtime.

**Step 5: Update CI to use `uv sync` instead of `pip install`, and commit `uv.lock`.**

```yaml
- name: Install uv
  run: curl -LsSf https://astral.sh/uv/install.sh | sh
- name: Sync dependencies
  run: uv sync --frozen
- name: Run tests
  run: uv run pytest
- name: Lint
  run: uvx ruff check .
```

**Step 6: Once the team has confirmed everything works for a sprint or two, delete `requirements.txt` and `requirements-dev.txt`.**

The old commands can be kept documented for a short transition period so nobody is stuck if something in the new flow needs debugging, then removed once the team trusts the new setup.

### **Old vs New — Command Mapping**

| Old command | New uv equivalent |
|---|---|
| `pip install -r requirements.txt` | `uv sync` |
| `pip install -r requirements-dev.txt` | `uv sync` (dev group is included automatically) |
| `pip install package-name` | `uv add package-name` |
| `pip install --dev package-name` | `uv add --dev package-name` |
| `python script.py` | `uv run python script.py` |
| `pytest` | `uv run pytest` |
| `pip freeze > requirements.txt` | `uv.lock` is generated and updated automatically |
| `source .venv/bin/activate` | (not needed) `uv run` does the equivalent |
| `pyenv install 3.12` | `uv python install 3.12` |
| `pipx install ruff` | `uv tool install ruff` |
| `pipx run ruff` | `uvx ruff` |
| `twine upload dist/*` | `uv publish` |
| `python -m build` | `uv build` |

## **Case Study 2: A Monorepo With Two Microservices**

**Scenario:** A team has two related services — a small `core` library shared between them, and a `web` service that consumes `core`. Both are in the same git repository, share a CI pipeline, and should always use the same versions of third-party dependencies like `fastapi` and `pydantic`.

```
monorepo/
├── pyproject.toml          # workspace root
├── uv.lock                  # single shared lockfile
├── core/
│   ├── pyproject.toml
│   └── src/core/__init__.py
└── web/
    ├── pyproject.toml
    └── src/web/main.py
```

Root `pyproject.toml`:

```toml
[project]
name = "monorepo"
version = "0.1.0"
requires-python = ">=3.11"

[tool.uv.workspace]
members = ["core", "web"]
```

`core/pyproject.toml`:

```toml
[project]
name = "core"
version = "0.1.0"
dependencies = ["pydantic>=2.7"]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/core"]
```

`web/pyproject.toml`:

```toml
[project]
name = "web"
version = "0.1.0"
dependencies = [
    "core",
    "fastapi>=0.115",
    "uvicorn>=0.30",
]

[tool.uv.sources]
core = { workspace = true }
```

Now the team has:

- One lockfile covering both services.
- `core` resolved as a local editable install inside the workspace, not a PyPI download.
- `uv sync` once, and both services are ready to run.
- `uv run --package web uvicorn web.main:app` to run just the web service.
- `uv run --package core pytest` to test just the core library.

The CI pipeline runs the same `uv sync --frozen` regardless of which service changed, and the lockfile guarantees both services always see the same `fastapi` version.

## **Case Study 3: A Data Science Notebook Project**

**Scenario:** A data scientist wants to keep a project's dependencies reproducible, but the project lives in a folder of Jupyter notebooks rather than a Python package. uv can manage a "non-package" project too.

```bash
uv init notebooks --bare
cd notebooks
uv add --dev jupyter pandas scikit-learn matplotlib
uv run jupyter lab
```

Resulting `pyproject.toml`:

```toml
[project]
name = "notebooks"
version = "0.1.0"
requires-python = ">=3.11"

[dependency-groups]
dev = [
    "jupyter>=1.0",
    "pandas>=2.2",
    "scikit-learn>=1.5",
    "matplotlib>=3.9",
]
```

When a teammate clones the project, they run `uv sync` and immediately have the same notebook environment. The `uv.lock` is committed, so even the matplotlib version is bit-for-bit identical.

A notebook can confirm which environment it is using by running:

```python
import sys
print(sys.executable)
# /path/to/notebooks/.venv/bin/python
```

If the path points into `.venv`, the notebook is using the locked environment, not a stray system Python.

## **Case Study 4: A Library With Optional Features**

**Scenario:** A small library called `mylib` can be used as a pure-Python helper, but gets a 10x speedup if `numpy` is installed, and supports YAML config files if `pyyaml` is installed. Both should be optional, advertised as extras, and not pulled in by default.

`mylib/pyproject.toml`:

```toml
[project]
name = "mylib"
version = "0.3.0"
requires-python = ">=3.9"

[project.optional-dependencies]
fast  = ["numpy>=1.26"]
yaml  = ["pyyaml>=6.0"]
all   = ["mylib[fast,yaml]"]

[dependency-groups]
dev = ["pytest>=8.0", "ruff>=0.6"]
```

In `mylib/__init__.py`, the optional dependencies are imported lazily so the package imports cleanly even when they are missing:

```python
def fast_mean(values):
    try:
        import numpy as np
    except ImportError as e:
        raise ImportError(
            "fast_mean requires the 'fast' extra: pip install mylib[fast]"
        ) from e
    return np.mean(values)
```

Users opt in:

```bash
pip install mylib                # just the core
pip install "mylib[fast]"        # with numpy
pip install "mylib[all]"         # everything
```

The maintainer runs the test matrix:

```bash
uv sync --no-dev                          # core only
uv sync --extra fast --no-dev             # with numpy
uv sync --all-extras --no-dev             # with everything
```

This is the cleanest way to publish a library that has a small core and optional performance or format features.

## **Case Study 5: Using `uv` in a Restricted CI Environment**

**Scenario:** A CI runner has no network access to PyPI but does have a populated uv cache. The job must install dependencies, run tests, and never touch the network.

```bash
# Pre-populated by the image build step earlier
ls /root/.cache/uv
# archives/  environments/  wheels-v4/  ...

# Inside the job
export UV_OFFLINE=1
export UV_NO_CACHE=1
uv sync --frozen --all-groups
uv run pytest
```

`UV_OFFLINE=1` blocks any network access during the resolve, and `--frozen` ensures `uv.lock` is the only source of truth. If `uv.lock` references a package that is not in the local cache, uv will fail with a clear error rather than silently reaching out to PyPI.

This pattern is common in air-gapped build systems, hermetic CI runners, and reproducible-build environments.

## **Things to Keep in Mind**

- **Always commit `uv.lock` for applications**, so every environment installs the exact same versions. This matches how `poetry.lock` is typically handled.
- **For a library** meant to be published and depended on by other projects, commit `uv.lock` for reproducible CI runs, but do not rely on shipping it to end users, since a library's actual dependency versions should be resolved by whatever project installs it, not fixed by the library's own lockfile.
- **Put `.venv/` in `.gitignore`**; it is a generated artifact, not something to version control.
- **Commit `.python-version`** so the whole team, and CI, uses the same interpreter version by default.
- **`requirements.txt` can be generated from `uv.lock` on the fly** if some external tool still strictly requires it, without going back to maintaining it by hand.
- **Migrate one small piece at a time** in an existing project rather than rewriting everything at once: get `pyproject.toml` and `uv sync` working first, confirm tests pass, then update Dockerfiles, CI configs, and any Makefile targets afterward.
- **`uv run` automatically re-syncs the environment** if `pyproject.toml` or `uv.lock` has changed since the last sync, so an environment drifting out of date silently is much less likely than with a manually managed venv.
- **For private package indexes**, such as an internal Artifactory or Nexus server, declare them under `[[tool.uv.index]]` in `pyproject.toml`, or pass `--index-url` / `--extra-index-url` flags directly. Authentication is read from environment variables (`UV_INDEX_<NAME>_USERNAME`, `UV_INDEX_<NAME>_PASSWORD`).
- **`uv sync` is exact by default** — it will remove any package that is not in the lockfile. Use `--inexact` if you want to keep tools you have installed outside uv. Note: `uv run` is the opposite — it is inexact by default, and accepts `--exact` for the strict behaviour.
- **`uv add` writes the loosest acceptable constraint** to `pyproject.toml`, then `uv.lock` holds the exact resolved version. Resist the urge to hand-edit hard pins into `pyproject.toml` unless a package is genuinely known to break; the lockfile is the right place for exact versions.
- **Workspaces share one lockfile.** Adding a package in any member's `pyproject.toml` and running `uv lock` updates versions for the whole workspace. Run `uv lock --check` in CI to make sure everyone has the same lockfile.
- **The `uv` cache is global.** On Linux/macOS it lives at `~/.cache/uv`; on Windows at `%LOCALAPPDATA%\uv`. The cache makes repeated installs near-instant. Use `UV_NO_CACHE=1` only in CI, never in normal use.

## **Common Gotchas**

- **Forgetting `--frozen` in CI** lets uv silently re-resolve and produce a different lockfile than what is committed, masking dependency bugs.
- **Using `uvx` for a project test command** runs the tool in an isolated environment that cannot see your project. If `pytest` then says "no tests ran", you almost certainly wanted `uv run pytest`.
- **Confusing `[project.optional-dependencies]` with `[dependency-groups]`**: extras are for end users of the library, groups are for maintainers. Installing the library with `pip install mylib` does not pull in any group.
- **Mixing `uv pip install` into a project that already has `uv.lock`**: it works, but it bypasses the lockfile, and the next `uv sync --exact` will remove whatever was installed. Use `uv add` instead.
- **A wrong `[project].name`** in `pyproject.toml` can clash with an installed package of the same name. The error is usually a `ModuleNotFoundError` or, worse, a silently-wrong import. Check `uv tree` to confirm the project name is what you think it is.
- **`requires-python` is a hard constraint.** Pinning `requires-python = ">=3.13"` in a project whose code uses 3.12-only syntax will fail to build wheels for 3.12. Set this to the lowest Python version you actually support.
- **`uv self update` only updates the binary** the installer manages. If you installed via `brew` or `pip`, use those tools' update commands instead (`brew upgrade uv`, `pip install --upgrade uv`).
- **Docker layer caching**: putting `uv sync` before `COPY` of the source code makes Docker reuse the dependency layer across builds. Put `pyproject.toml` and `uv.lock` in their own `COPY` step, run `uv sync`, then `COPY` the rest of the source.

## **Best Practices**

- **Use `uv init --bare`** when adding uv to an existing project, instead of `uv init` which creates a starter `main.py` you do not need.
- **Prefer `uv run` over activating a venv.** It is one command, no shell state, and the same in scripts and CI.
- **Use `uv add` for every dependency change**, even "just installing one thing to try it out". The lockfile is the source of truth, and the only way to update it correctly is through `uv add` / `uv remove`.
- **Set `requires-python` early.** It is the most important constraint in `pyproject.toml` and affects every lockfile resolution.
- **Group your dev dependencies by purpose.** `dev` for general testing and linting, `docs` for documentation tools, `notebooks` for Jupyter extras, and so on. This lets CI install exactly what a job needs.
- **Add a `uv.lock`-check step to CI.** Something like `uv lock --check` ensures no one accidentally committed a change to `pyproject.toml` without committing the corresponding `uv.lock`.
- **Use `uv build` and `uv publish`** instead of `python -m build` and `twine` for new projects. They produce identical artifacts with fewer commands.
- **In Docker, use the multi-stage pattern** from Case Study 1. The build stage is the only one that needs network access, the runtime stage is just Python plus a prebuilt `.venv`.
- **Pin a `uv` version in CI** for reproducibility. The official installer lets you pin: `curl -LsSf https://astral.sh/uv/0.5.0/install.sh | sh`.

## **Quick Reference Summary**

### **Project Commands**

| Command | Purpose |
|---|---|
| `uv init [name]` | Start a new uv-managed project |
| `uv init --bare` | Add uv to an existing project without scaffolding |
| `uv add <pkg>` | Add a dependency, updates `pyproject.toml` and `uv.lock` |
| `uv add --dev <pkg>` | Add a development-only dependency |
| `uv add --optional <pkg>` | Add an optional extra |
| `uv add --group <name> <pkg>` | Add to a named dependency group |
| `uv remove <pkg>` | Remove a dependency |
| `uv sync` | Install everything to match `pyproject.toml` and `uv.lock` |
| `uv sync --frozen --no-dev` | Fast, reproducible install for CI/production |
| `uv sync --inexact` | Install required packages, do not remove extras |
| `uv sync --all-extras` | Install all optional dependencies |
| `uv run <cmd>` | Run a command inside the project's managed environment |
| `uv run --frozen <cmd>` | Run without re-resolving the lockfile |
| `uv lock` | Regenerate the lockfile without installing |
| `uv lock --upgrade` | Upgrade all locked packages to the latest allowed versions |
| `uv lock --upgrade-package <pkg>` | Upgrade just one package |
| `uv lock --check` | Verify the lockfile is up to date |
| `uv tree` | Show the full dependency tree |
| `uv version` | Show or bump the project version |
| `uv build` | Build sdist and wheel |
| `uv publish` | Publish to PyPI (or `--publish-url` for Test PyPI) |
| `uv format` | Format code with the built-in Ruff formatter |
| `uv check` | Type-check the project with `ty` |
| `uv audit` | Check locked deps for known vulnerabilities |
| `uv export` | Export `uv.lock` to `requirements.txt`, `pylock.toml`, or SBOM |

### **Python and Tools**

| Command | Purpose |
|---|---|
| `uv python install <ver>` | Download and install a specific Python version |
| `uv python list` | Show installed and available Python versions |
| `uv python pin <ver>` | Pin the Python version for this project |
| `uvx <tool>` | Run a tool from a package without installing it into the project |
| `uv tool install <pkg>` | Install a tool permanently on `PATH` |
| `uv tool list` | List installed tools |
| `uv tool uninstall <pkg>` | Remove an installed tool |
| `uv venv` | Create a plain virtual environment |
| `uv venv --python 3.12` | Create a venv with a specific Python version |

### **pip-Compatible Interface**

| Command | Equivalent to |
|---|---|
| `uv pip install <pkg>` | `pip install <pkg>` |
| `uv pip install -r requirements.txt` | `pip install -r requirements.txt` |
| `uv pip uninstall <pkg>` | `pip uninstall <pkg>` |
| `uv pip list` | `pip list` |
| `uv pip freeze` | `pip freeze` |
| `uv pip compile requirements.in -o requirements.txt` | `pip-compile` |
| `uv pip sync requirements.txt` | `pip-sync` |

### **Common Flag Patterns**

| Need | Flags |
|---|---|
| Reproducible CI install | `uv sync --frozen --no-dev` |
| Lockfile-only check | `uv lock --check` |
| Run without re-sync | `uv run --no-sync <cmd>` |
| Strict lockfile at run time | `uv run --locked <cmd>` |
| Install all extras | `uv sync --all-extras` |
| Skip dev tools | `uv sync --no-dev` |
| Use a custom index | `--index-url https://my.pypi/ simple/` |
| Upgrade everything | `uv lock --upgrade` |
| Upgrade one package | `uv lock --upgrade-package <pkg>` |

### **Decision Cheat Sheet**

| Situation | Use |
|---|---|
| Quick one-off tool (lint, format, inspect) | `uvx` |
| Daily-driver tool (ruff, black, httpie) | `uv tool install` |
| Project's own tests, type checks, scripts | `uv run` |
| Pure-Python project with no `pyproject.toml` | `uv pip` |
| New package to publish to PyPI | `uv init` + `uv add` + `uv build` + `uv publish` |
| Migrate from `requirements.txt` | `uv init --bare` + `uv add -r requirements.txt` |
| Multi-package monorepo | Workspace with `tool.uv.workspace` |
| Pin a different Python | `uv python pin 3.12` |

## **Practice and Next Steps**

Small exercises to lock the concepts in:

- Take a small existing script that currently uses a manually managed venv and `requirements.txt`, and migrate it to `uv init --bare` plus `uv add -r requirements.txt`. Commit `uv.lock` and confirm a fresh clone + `uv sync` reproduces the environment exactly.
- Add a dev-only dependency group with `pytest`, then run it with `uv run pytest` without ever activating a virtual environment manually.
- Practice `uv lock --upgrade-package` on a single dependency and inspect the diff in `uv.lock` before committing it.
- Try `uvx` to run a linter or formatter on a project without adding it as a dependency at all, then try `uv tool install` for the same tool and notice the second form puts the command on `PATH`.
- Convert a flat-layout project you already have into the `src/` layout and confirm `uv sync` still works. Add `[tool.uv] package = true` (or equivalent) so uv treats the source directory as a real package.
- Set up a workspace with two small members and a shared lockfile, then run `uv run --package <name> pytest` from the workspace root to see targeted execution.
- Run `uv build` on a small library and inspect the contents of `dist/`. Then run `uv publish --publish-url https://test.pypi.org/legacy/` to push it to Test PyPI, and `pip install --index-url https://test.pypi.org/simple/ your-package` in a separate venv to confirm it works.
- Add `uv lock --check` and `uv run pytest` to a GitHub Actions workflow and see the lockfile check catch a missing commit.
- Try `uv export --format requirements-txt` and `uv export --format cyclonedx1.5` to see what each output looks like, then feed the SBOM into a security tool.
- Pin uv itself in a CI workflow to a specific version and observe the deterministic build it produces.

After these, the natural next topics are: monorepo CI patterns, multi-stage Dockerfiles with uv, mirroring PyPI for air-gapped environments, and using uv in a JupyterHub / Dask / MLflow workflow.
