#!/usr/bin/env python3
from __future__ import annotations
# not using pytest here to avoid interference from actual pytest
import contextlib
import os
from pathlib import Path
import re
import shutil
import sys
import subprocess
from tempfile import TemporaryDirectory
from typing import Iterator

THISDIR = Path(__file__).absolute().parent
GIT_ROOT = THISDIR.parent

# only available since python 3.11
class contextlib_chdir(contextlib.AbstractContextManager):
    def __init__(self, path):
        self.path = path
        self._old_cwd = []

    def __enter__(self):
        self._old_cwd.append(os.getcwd())
        os.chdir(self.path)

    def __exit__(self, *excinfo):
        os.chdir(self._old_cwd.pop())


@contextlib.contextmanager
def fixture() -> Iterator[Path]:
    with TemporaryDirectory() as td:
        root = Path(td)
        shutil.copy(GIT_ROOT / 'pytest.ini' , root / 'pytest.ini')
        shutil.copy(GIT_ROOT / 'conftest.py', root / 'conftest.py')
        shutil.copytree(THISDIR / 'testdata' / 'src', root / 'src')
        with contextlib_chdir(root):
            yield root

def run(package: str) -> list[str]:
    # returns the tests that ran
    output = subprocess.check_output([sys.executable, '-m', 'pytest', '--pyargs', package, '-s'], text=True, stderr=subprocess.STDOUT)
    return sorted(re.findall(r'RUNNING ([\w.]+)', output))


def test_basic() -> None:
    # should collect/run all tests
    with fixture() as root:
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
    with fixture() as root:
        res = run('mypkg.a')
        assert res == [
            'mypkg.a.aa.main',
            'mypkg.a.main',
        ], res


def test_subpackage_2() -> None:
    with fixture() as root:
        res = run('mypkg.a.aa')
        assert res == [
            'mypkg.a.aa.main',
        ], res


def test_module_1() -> None:
    with fixture() as root:
        res = run('mypkg.main')
        assert res == [
            'doctest',
            'mypkg.main',
        ], res


def test_module_2() -> None:
    # checks that it works with __init__.py
    with fixture() as root:
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
