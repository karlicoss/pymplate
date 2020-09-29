def test():
    assert True # dummy test


## just check that mypy works
class A:
    pass

import typing
if typing.TYPE_CHECKING:
    # sigh. apparently reveal_type is making mypy fail
    # reveal_type(A)
    pass
##
