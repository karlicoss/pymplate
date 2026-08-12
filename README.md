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

For a targeted test run:

```bash
tox -e tests -- -k <pattern>
```

`tox` is the supported task runner.
The `noxfile.py` configuration is experimental and is not part of the normal workflow.

The `.ci/run` entrypoint is for GitHub Actions only.
It runs tox through `uv tool run --with tox-uv`; use direct `tox -e ...` commands for local development.

The configured `tox-uv` lock runner creates or updates an ignored `uv.lock`.
The lockfile is deliberately not tracked so CI resolves current dependency versions; do not commit it.

## Test Layout

`pyproject.toml` intentionally configures pytest to collect all `*.py` files and doctests.
Ordinary project tests should live next to implementation modules rather than under `tests/`.

`tests/test_pytest.py` is a self-check for pytest namespace-package discovery. It runs without pytest
as the outer test runner first, then invokes pytest in a temporary package tree to verify collection
behavior.

## Releases

The release script is `.ci/release`.

To preview commit-level release notes and open a prefilled GitHub release form without creating a
tag or release:

```bash
.ci/prepare-github-release
```

This fetches the remote default branch and the latest remote release tag, then runs `git-cliff`
through an ad-hoc Nix invocation.
Both the generated notes and the GitHub release target are based on the fetched default branch
rather than the currently checked-out branch.
By default, the proposed tag increments the minor version and uses today's date in `YYYYMMDD` form
for the final component. A repository without release tags starts at `v0.1.YYYYMMDD`. If an existing
tag does not have `vMAJOR.MINOR.SUFFIX` form, pass `--tag` explicitly. The generated release title is
`<tag>: rolling release`.

Override these defaults with:

```bash
.ci/prepare-github-release --tag v0.3.20260812 --title 'v0.3.20260812: summary'
```

To print the preview and URL without opening a browser:

```bash
.ci/prepare-github-release --no-open
```

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
