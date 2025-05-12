import typing

if typing.TYPE_CHECKING:
    # sigh. apparently reveal_type is making mypy fail
    # reveal_type(__file__)
    pass


def test_module_name() -> None:
    # just in case because pytest might have some shenanigans with test module names depending on args..
    assert __name__ == 'karlicoss_pymplate.module'


def check_doctest() -> None:
    """
    >>> 1 + 2
    3
    """
    # this doctest should be collected by pytest and run
