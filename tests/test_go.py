from goban import Go, Status
from goban.goban import Goban


def test_get_status():
    goban = Goban(
        [
            ".o.",
            "..#",
        ]
    )
    go = Go(goban)

    assert go.get_status(0, 0) == Status.EMPTY
    assert go.get_status(1, 0) == Status.WHITE
    assert go.get_status(2, 1) == Status.BLACK
    assert go.get_status(-1, -1) == Status.OUT


def test_is_taken():
    goban = Goban(
        [
            "oo.",
            "##o",
            "o#o",
            "#o.",
        ]
    )
    go = Go(goban)

    assert go.is_taken(0, 0) is False
    assert go.is_taken(1, 1) is True
    assert go.is_taken(0, 2) is True
