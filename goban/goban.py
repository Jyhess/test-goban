from typing import List

from .invalid_goban_error import InvalidGobanError
from .invalid_position_error import InvalidPositionError
from .status import Status


class Goban:
    def __init__(self, goban: List[str]) -> None:
        if not goban:
            raise InvalidGobanError("Goban must not be empty", "", -1)
        for i, line in enumerate(goban):
            if not line:
                raise InvalidGobanError("Goban must not be empty", line, i)
            if len(line) != len(goban[0]):
                raise InvalidGobanError("Goban must be a rectangle", line, i)
            if not all(c in "o#." for c in line):
                raise InvalidGobanError("Goban must only contain o, # or .", line, i)

        self._goban = goban

    def get_status(self, x: int, y: int) -> Status:
        """
        Get the status of a given position

        Args:
            x: the x coordinate
            y: the y coordinate

        Returns:
            a Status
        """
        if (
            not self._goban
            or x < 0
            or y < 0
            or y >= len(self._goban)
            or x >= len(self._goban[0])
        ):
            return Status.OUT
        elif self._goban[y][x] == ".":
            return Status.EMPTY
        elif self._goban[y][x] == "o":
            return Status.WHITE
        elif self._goban[y][x] == "#":
            return Status.BLACK
        raise ValueError(f"Unknown goban value {self._goban[y][x]}")

    def is_taken(self, x: int, y: int) -> bool:
        status = self.get_status(x, y)
        if status == Status.OUT:
            raise InvalidPositionError("Position is out of goban", x, y)
        if status == Status.EMPTY:
            raise InvalidPositionError("Position is empty", x, y)
        color = self.get_status(x, y)
        opponent_color = Status.WHITE if color == Status.BLACK else Status.BLACK
        if (
            self.get_status(x - 1, y) == opponent_color
            and self.get_status(x + 1, y) == opponent_color
            and self.get_status(x, y - 1) == opponent_color
            and self.get_status(x, y + 1) == opponent_color
        ):
            return True
        return False
