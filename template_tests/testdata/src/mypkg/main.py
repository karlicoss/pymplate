def test():
    print("RUNNING", __name__)


def function_with_doctest():
    """Just checking doctest
    >>> import sys
    >>> print("RUNNING", "doctest", file=sys.stderr)
    >>> 1 + 1
    2
    """
    pass
