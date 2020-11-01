def test():
    # dummy test. it's also useful to have regardless so pytest is configured early on (it fails on no tests)
    assert True


## just check that mypy works
class A:
    pass

import typing
if typing.TYPE_CHECKING:
    # sigh. apparently reveal_type is making mypy fail
    # reveal_type(A)
    pass
##
