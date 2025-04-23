import pytest

from goban import InvalidPositionError
from goban.goban import Goban
from goban.position_analyzer import PositionAnalyzer


def make_analyser(goban_data: list[str]) -> PositionAnalyzer:
    goban = Goban(goban_data)
    return PositionAnalyzer(goban)


def test_is_taken_empty():
    goban = [
        ".o.",
        "..#",
    ]
    analyser = make_analyser(goban)
    with pytest.raises(InvalidPositionError) as e:
        analyser.is_taken(0, 0)
    assert str(e.value) == "Position is empty at (0,0)"


def test_is_taken_invalid():
    goban_data = [
        ".o.",
        "..#",
    ]
    analyser = make_analyser(goban_data)
    with pytest.raises(InvalidPositionError) as e:
        analyser.is_taken(-1, 0)
    assert str(e.value) == "Position is out of goban at (-1,0)"


def test_white_is_taken_when_surrounded_by_black():
    goban_data = [
        ".#.",
        "#o#",
        ".#.",
    ]
    analyser = make_analyser(goban_data)

    assert analyser.is_taken(1, 1) is True


def test_white_is_not_taken_when_it_has_a_liberty_on_top():
    goban_data = [
        "...",
        "#o#",
        ".#.",
    ]
    analyser = make_analyser(goban_data)

    assert analyser.is_taken(1, 1) is False


def test_white_is_not_taken_when_it_has_a_liberty_on_left():
    goban_data = [
        ".#.",
        ".o#",
        ".#.",
    ]
    analyser = make_analyser(goban_data)

    assert analyser.is_taken(1, 1) is False


def test_white_is_not_taken_when_it_has_a_liberty_on_right():
    goban_data = [
        ".#.",
        "#o.",
        ".#.",
    ]
    analyser = make_analyser(goban_data)

    assert analyser.is_taken(1, 1) is False


def test_white_is_not_taken_when_it_has_a_liberty_on_bottom():
    goban_data = [
        ".#.",
        "#o#",
        "...",
    ]
    analyser = make_analyser(goban_data)

    assert analyser.is_taken(1, 1) is False


@pytest.mark.parametrize("x, y", [(0, 1), (1, 1), (1, 2)])
def test_black_shape_is_taken_when_surrounded(x, y):
    goban_data = [
        "oo.",
        "##o",
        "o#o",
        ".o.",
    ]
    analyser = make_analyser(goban_data)

    assert analyser.is_taken(x, y) is True


@pytest.mark.parametrize("x, y", [(0, 1), (1, 1), (1, 2)])
def test_black_shape_is_not_taken_when_it_has_a_liberty(x, y):
    goban_data = [
        "oo.",
        "##.",
        "o#o",
        ".o.",
    ]
    analyser = make_analyser(goban_data)

    assert analyser.is_taken(x, y) is False


@pytest.mark.parametrize("x, y", [(0, 1), (0, 2), (1, 1), (1, 2)])
def test_square_shape_is_taken(x, y):
    goban_data = [
        "oo.",
        "##o",
        "##o",
        "oo.",
    ]
    analyser = make_analyser(goban_data)

    assert analyser.is_taken(x, y) is True


@pytest.mark.parametrize("x, y", [(0, 0), (4, 0), (0, 4), (4, 4)])
def test_corner_shape_is_taken(x, y):
    goban_data = [
        "o#.o#",
        "#...o",
        ".....",
        "o...#",
        "#o.#o",
    ]
    analyser = make_analyser(goban_data)

    assert analyser.is_taken(x, y) is True


@pytest.mark.parametrize("x, y", [(0, 0), (4, 0), (0, 4), (4, 4)])
def test_corner_shape_is_not_taken(x, y):
    goban_data = [
        "o#.o#",
        "o....",
        ".....",
        "o...#",
        "#...o",
    ]
    analyser = make_analyser(goban_data)

    assert analyser.is_taken(x, y) is False


@pytest.mark.parametrize("x, y", [(1, 1), (1, 2), (3, 3)])
def test_white_shape_is_not_taken_when_it_has_an_eye(x, y):
    goban_data = [
        ".###.",
        "#ooo#",
        "#o.o#",
        "#ooo#",
        ".###.",
    ]
    analyser = make_analyser(goban_data)

    assert analyser.is_taken(x, y) is False


@pytest.mark.parametrize("x, y", [(1, 1), (1, 2), (3, 3)])
def test_white_shape_is_taken_when_eye_is_filled(x, y):
    goban_data = [
        ".###.",
        "#ooo#",
        "#o#o#",
        "#ooo#",
        ".###.",
    ]
    analyser = make_analyser(goban_data)

    assert analyser.is_taken(x, y) is True
