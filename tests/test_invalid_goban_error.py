from goban import InvalidGobanError


def test_str():
    error = InvalidGobanError("Invalid goban", "o#.", 1)
    assert str(error) == "Invalid goban at line 1: o#."


def test_str_long_line():
    error = InvalidGobanError("Invalid goban", "o#..o#..o#..", 1)
    assert str(error) == "Invalid goban at line 1: o#..o#..o#"


def test_str_negative_index():
    error = InvalidGobanError("Invalid goban", "o#.", -1)
    assert str(error) == "Invalid goban"
