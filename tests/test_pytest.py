#!/usr/bin/env python3
from __future__ import annotations

# not using pytest here to avoid interference from actual pytest
import contextlib
import os
import re
import shlex
import shutil
import subprocess
import sys
from collections.abc import Iterator
from pathlib import Path
from tempfile import TemporaryDirectory

THISDIR = Path(__file__).absolute().parent
GIT_ROOT = THISDIR.parent


# only available since python 3.11
class contextlib_chdir(contextlib.AbstractContextManager):
    def __init__(self, path):
        self.path = path
        self._old_cwd = []

    def __enter__(self):
        self._old_cwd.append(Path.cwd())
        os.chdir(self.path)

    def __exit__(self, *excinfo):
        os.chdir(self._old_cwd.pop())


@contextlib.contextmanager
def fixture() -> Iterator[Path]:
    with TemporaryDirectory() as td:
        root = Path(td)
        shutil.copy(GIT_ROOT / 'pytest.ini', root / 'pytest.ini')
        # conftest isn't necessary anymore! pytest 9 supports it out of box
        # shutil.copy(GIT_ROOT / 'conftest.py', root / 'conftest.py')
        shutil.copytree(THISDIR / 'testdata' / 'src', root / 'src')
        with contextlib_chdir(root):
            yield root


def run(package: str) -> list[str]:
    # returns the tests that ran
    cmd = [sys.executable, '-m', 'pytest', '--pyargs', package, '-s']
    print('pytest command: ', shlex.join(cmd), file=sys.stderr)
    # NOTE: this resolve() here is important for windows!
    # otherwise for some reason sys.path under pytest ends up with something like
    # 'C:\\Users\\RUNNER~1\\...', and that messes up package name discovery
    # This is until it gets to src dir which is in 'current' directory due to python3 -m pytest and succeeds
    #  , but as a result we end up with src.mypkgs.. names which we don't want
    src_path = str(Path('src').resolve())
    output = subprocess.check_output(
        cmd, text=True, stderr=subprocess.STDOUT, env={'PYTHONPATH': src_path, **os.environ}
    )
    return sorted(re.findall(r'RUNNING ([\w.]+)', output))


def test_basic() -> None:
    # should collect/run all tests
    with fixture() as _root:
        res = run('mypkg')
        assert res == [
            'doctest',
            'mypkg.a.aa.main',
            'mypkg.a.main',
            'mypkg.b.b',
            'mypkg.c',
            'mypkg.main',
        ], res


def test_subpackage_1() -> None:
    with fixture() as _root:
        res = run('mypkg.a')
        assert res == [
            'mypkg.a.aa.main',
            'mypkg.a.main',
        ], res


def test_subpackage_2() -> None:
    with fixture() as _root:
        res = run('mypkg.a.aa')
        assert res == [
            'mypkg.a.aa.main',
        ], res


def test_module_1() -> None:
    with fixture() as _root:
        res = run('mypkg.main')
        assert res == [
            'doctest',
            'mypkg.main',
        ], res


def test_module_2() -> None:
    # checks that it works with __init__.py
    with fixture() as _root:
        res = run('mypkg.c')
        assert res == [
            'mypkg.c',
        ], res


def main() -> None:
    tests = [
        test_basic,
        test_subpackage_1,
        test_subpackage_2,
        test_module_1,
        test_module_2,
    ]
    for test in tests:
        print("RUNNING", test)
        test()


if __name__ == '__main__':
    main()
