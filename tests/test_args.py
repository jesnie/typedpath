from typedpath import NO_ARGS, Args, withargs


def test_withargs__empty() -> None:
    assert Args({}) == withargs()


def test_withargs() -> None:
    assert Args({"foo": 1, "bar": "baz"}) == withargs(foo=1, bar="baz")


def test_no_args() -> None:
    assert Args({}) == NO_ARGS
