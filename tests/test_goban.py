import pytest

from goban import InvalidGobanError, Status
from goban.goban import Goban


def test_goban_without_data():
    with pytest.raises(InvalidGobanError) as e:
        Goban(None)
    assert str(e.value) == "Goban must not be empty"

    with pytest.raises(InvalidGobanError) as e:
        Goban([])
    assert str(e.value) == "Goban must not be empty"

    with pytest.raises(InvalidGobanError) as e:
        Goban([""])
    assert str(e.value) == "Goban must not be empty at line 0: "

    with pytest.raises(InvalidGobanError) as e:
        Goban([".", ""])
    assert str(e.value) == "Goban must not be empty at line 1: "


def test_goban_with_invalid_characters():
    with pytest.raises(InvalidGobanError) as e:
        Goban(
            [
                "foo",
            ]
        )
    assert str(e.value) == "Goban must only contain o, # or . at line 0: foo"

    with pytest.raises(InvalidGobanError) as e:
        Goban(
            [
                ".o#",
                "ooX",
            ]
        )
    assert str(e.value) == "Goban must only contain o, # or . at line 1: ooX"


def test_goban_with_inconsistent_lines():
    with pytest.raises(InvalidGobanError) as e:
        Goban(
            [
                ".o#",
                "oo",
            ]
        )
    assert str(e.value) == "Goban must be a rectangle at line 1: oo"

    with pytest.raises(InvalidGobanError) as e:
        Goban(
            [
                ".o#",
                "o",
            ]
        )
    assert str(e.value) == "Goban must be a rectangle at line 1: o"


def test_get_status():
    goban = Goban(
        [
            ".o.",
            "..#",
        ]
    )

    assert goban.get_status(0, 0) == Status.EMPTY
    assert goban.get_status(1, 0) == Status.WHITE
    assert goban.get_status(2, 1) == Status.BLACK
    assert goban.get_status(-1, -1) == Status.OUT
    assert goban.get_status(0, -1) == Status.OUT
    assert goban.get_status(-1, 0) == Status.OUT
    assert goban.get_status(4, 0) == Status.OUT
    assert goban.get_status(0, 3) == Status.OUT
    assert goban.get_status(4, 3) == Status.OUT
