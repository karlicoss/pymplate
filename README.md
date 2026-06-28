# pymplate

My opinionated Python project template.

The template is meant to be small, current, and practical. It uses modern Python packaging via
`pyproject.toml`, keeps tests close to source modules, and relies on the same local toolchain as CI.

## What It Includes

- `src/` layout with an implicit namespace package.
- Packaging via `hatchling` and `hatch-vcs`.
- Dependency management and isolated tool runs via `uv`, `tox`, and `tox-uv`.
- Test discovery through `pytest --pyargs`, including doctests and source files that do not follow
  the usual `test_*.py` naming convention.
- Linting and formatting with `ruff`.
- Type checking with `mypy` and `ty`.
- GitHub Actions CI across Linux, macOS, Windows, and supported Python versions.
- PyPI/TestPyPI publishing through `uv publish` and GitHub Trusted Publishing.

## Local Checks

Run the narrowest tox environment that validates your change:

```bash
tox -e ruff
tox -e format
tox -e tests
tox -e mypy
tox -e ty
```

For ruff preview checks:

```bash
tox -e ruff -- --preview
```

The CI entrypoint is `.ci/run`. It currently runs tox through `uv tool run --with tox-uv`, and CI uses
it directly:

```bash
bash .ci/run
```

Prefer direct `tox -e ...` commands for ordinary local development, and check `.ci/run` when changing CI
or tox behavior.

## Test Layout

`pyproject.toml` intentionally configures pytest to collect all `*.py` files and doctests. This supports
keeping tests next to implementation modules instead of adding separate files under `tests/`.

`tests/test_pytest.py` is a self-check for pytest namespace-package discovery. It runs without pytest
as the outer test runner first, then invokes pytest in a temporary package tree to verify collection
behavior.

## Releases

The release script is `.ci/release`.

Manual publishing requires:

```bash
UV_PUBLISH_TOKEN=... .ci/release
```

For TestPyPI:

```bash
UV_PUBLISH_TOKEN=... .ci/release --use-test-pypi
```

In GitHub Actions, publishing uses Trusted Publishing instead of an API token:

- commits to the repository default branch publish to TestPyPI;
- `v*` release tags publish to PyPI.

The workflow lives in `.github/workflows/main.yml`.
