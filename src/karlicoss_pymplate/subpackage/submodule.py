def test() -> None:
    # dummy test. it's also useful to have regardless so pytest is configured early on (it fails on no tests)
    assert True

    # check names because pytest might mess this up (also see conftest.py for some hacks)
    assert __package__ == 'karlicoss_pymplate.subpackage'
    assert __name__    == 'karlicoss_pymplate.subpackage.submodule'


## just check that mypy works
class A:
    pass

import typing
if typing.TYPE_CHECKING:
    # sigh. apparently reveal_type is making mypy fail
    # reveal_type(A)
    pass
##
