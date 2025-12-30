import os
from pathlib import Path

import nox  # ty: ignore[unresolved-import]

nox.options.default_venv_backend = "uv"

if (NOX_BASE := os.environ.get("NOX_BASE")) is not None:
    # Prevent .nox from crapping into project directory if user prefers
    # This is to avoid creating virtualenvs with tons of files if projects are synced (e.g. Dropbox).
    project_path = Path(__file__).absolute().parent
    project_path = project_path.relative_to(project_path.anchor)
    nox.options.envdir = Path(NOX_BASE) / project_path

nox.options.reuse_existing_virtualenvs = True  #  not sure, but this is tox default, so keeping for consistency

nox.options.error_on_external_run = True  # not sure about this one, consistency with tox for now


# do not add current working directory to pythonpath
# generally this is more robust and safer, prevents weird issues later on
os.environ['PYTHONSAFEPATH'] = '1'


PYPROJECT = nox.project.load_toml()
PACKAGE_NAME = PYPROJECT["project"]["name"]


def _uv_sync(session: nox.Session, *sync_args: str) -> None:
    session.run_install(
        # TODO hmm this updates lock file in project dir, a bit annoying?..
        # currently uv doesn't allow custom lock file, see this issue https://github.com/astral-sh/uv/issues/6830
        # also this would prevent parallelism?
        "uv", "sync",
        *sync_args,
        f"--python={session.virtualenv.location}",
        env={
            "UV_PROJECT_ENVIRONMENT": session.virtualenv.location,
        },
    )  # fmt: skip


# TODO could do some dynamic magic to just have a single uv run command but split into install and run bits?
def _uv_install(session: nox.Session, *install_args: str) -> None:
    session.run_install(
        "uv", "pip", "install",
        "--editable", ".",
        *install_args,
        f"--python={session.virtualenv.location}",
        env={
            "UV_PROJECT_ENVIRONMENT": session.virtualenv.location,
        },
    )  # fmt: skip


@nox.session
def ruff(session: nox.Session) -> None:
    _uv_install(session, "--group", "testing")

    session.run(
        "python", "-m", "ruff",
        "check",
        *session.posargs,
    )  # fmt: skip


@nox.session
def tests(session: nox.Session) -> None:
    _uv_install(session, "--group", "testing")

    session.run("python", "tests/test_pytest.py")  # check pytest.ini/conftest

    # posargs allow test filtering, e.g. tox ... -- -k test_name
    session.run(
        "python", "-m", "pytest",
        "--pyargs", PACKAGE_NAME,
        *session.posargs,
    )  # fmt: skip


@nox.session
def mypy(session: nox.Session) -> None:
    _uv_install(session, "--group", "typecheck")

    # todo later could just run it only on ubuntu directly instead of github actions hack
    ci_mypy_coverage = os.environ.get("CI_MYPY_COVERAGE", "").split()

    session.run(
        "python", "-m", "mypy", "--no-install-types",
        "-p", PACKAGE_NAME,
        "--txt-report" , ".coverage.mypy",
        "--html-report", ".coverage.mypy",
        # this is for github actions to upload to codecov.io
        # sadly xml coverage crashes on windows... so we need to disable it
        *ci_mypy_coverage,
        *session.posargs,
    )  # fmt: skip


@nox.session
def ty(session: nox.Session) -> None:
    _uv_install(session, "--group", "typecheck")

    session.run(
        "python", "-m", "ty",
        "check",
        *session.posargs,
    )  # fmt: skip


# Nice things
# - can just put "import pdb; pdb.set_trace()" to debug
# - was trivial to read project name from pyproject.toml
# - VERY easy to reuse code etc for once
# ?
# - seems like nox just passes all env variables https://github.com/wntrblm/nox/issues/886
#   not sure if generally good idea, but I guess fine for now!
# - TODO ugh doesn't support running in parallel? https://github.com/wntrblm/nox/issues/544

# session.run("ty", "check", *session.posargs, env={"PYTHONSAFEPATH": "1"})
