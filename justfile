# NOTE: justfile is only used for adhoc stuff -- CI relies on tox for proper isolation.

# Pass recipe arguments to the shell as "$@", which preserves their quoting.
set positional-arguments

pkg    := "karlicoss_pymplate"

# Fast static checks suitable for running before a commit
[parallel, group('main')]
precommit: ruff format ty

# All static checks (default)
[default, parallel, group('main')]
lint     : precommit mypy

# All checks, including tests
[parallel, group('main')]
check    : lint test

# Apply ruff & format fixes
[group('main')]
fix      : ruff-fix format-fix  # sequential because both modify files

# The typecheck group includes testing, so one sync prepares every recipe.
@_sync:
    uv sync --no-default-groups --group typecheck

python := "uv run --no-sync python"  # recipes depend on _sync, so skip uv run's own sync


@format     *args: _sync
    {{python}} -m ruff   format --diff "$@"
@format-fix *args: _sync
    {{python}} -m ruff   format        "$@"
@mypy       *args: _sync
    {{python}} -m mypy                 "$@"
@ruff       *args: _sync
    {{python}} -m ruff   check         "$@"
@ruff-fix   *args: _sync
    {{python}} -m ruff   check --fix   "$@"
@test       *args: _sync
    {{python}} -m pytest               "$@"
@ty         *args: _sync
    {{python}} -m ty     check         "$@"

# Run the package.
[group('entrypoints')]
@run        *args:  # runtime deps only, so plain uv run instead of _sync
    uv run python -m "{{pkg}}" "$@"
