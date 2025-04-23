import pytest

from goban import Goban, InvalidGobanError, Status


def test_goban_without_data() -> None:
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


def test_goban_with_invalid_characters() -> None:
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


def test_goban_with_inconsistent_lines() -> None:
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


def test_get_status() -> None:
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


def test_white_is_taken_when_surrounded_by_black() -> None:
    goban = Goban(
        [
            ".#.",
            "#o#",
            ".#.",
        ]
    )

    assert goban.is_taken(1, 1) is True


def test_white_is_not_taken_when_it_has_a_liberty() -> None:
    goban = Goban(
        [
            "...",
            "#o#",
            ".#.",
        ]
    )

    assert goban.is_taken(1, 1) is False


# TODO Add case out of border
def test_black_shape_is_taken_when_surrounded() -> None:
    goban = Goban(
        [
            "oo.",
            "##o",
            "o#o",
            ".o.",
        ]
    )

    assert goban.is_taken(0, 1) is True
    assert goban.is_taken(1, 1) is True
    assert goban.is_taken(1, 2) is True


# TODO Add case out of border
def test_black_shape_is_not_taken_when_it_has_a_liberty() -> None:
    goban = Goban(
        [
            "oo.",
            "##.",
            "o#o",
            ".o.",
        ]
    )

    assert goban.is_taken(0, 1) is False
    assert goban.is_taken(1, 1) is False
    assert goban.is_taken(1, 2) is False


# TODO Add case out of border
def test_square_shape_is_taken() -> None:
    goban = Goban(
        [
            "oo.",
            "##o",
            "##o",
            "oo.",
        ]
    )

    assert goban.is_taken(0, 1) is True
    assert goban.is_taken(0, 2) is True
    assert goban.is_taken(1, 1) is True
    assert goban.is_taken(1, 2) is True


# TODO Add case 4 corners without liberty


# TODO Add case 4 corners with 1 liberty
