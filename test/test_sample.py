import pytest

def inc(x):
    return x + 1


def test_answer():
    assert inc(3) == 4

def f():
    raise SystemExit(1)


def test_mytest():
    with pytest.raises(SystemExit):
        f()