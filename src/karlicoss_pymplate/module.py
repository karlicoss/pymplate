import typing
if typing.TYPE_CHECKING:
    # sigh. apparently reveal_type is making mypy fail
    # reveal_type(__file__)
    pass

# NOTE: this doesn't work with tox -e py3, it thinks that the package name here is module.py and can't do a relative import
# https://github.com/pytest-dev/pytest/issues/1927
# https://github.com/pytest-dev/pytest/issues/2371
# from .subpackage import test
