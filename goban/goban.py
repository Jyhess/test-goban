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
        form = {(x, y)}
        neighbors_checked: set[tuple[int, int]] = set()
        return self._is_taken(x, y, form, neighbors_checked, color, opponent_color)

    def _is_taken(
        self,
        x: int,
        y: int,
        form: set[tuple[int, int]],
        neighbors_checked: set[tuple[int, int]],
        color: Status,
        opponent_color: Status,
    ) -> bool:
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            coordinates = (x + dx, y + dy)
            if coordinates in neighbors_checked:
                continue
            if coordinates in form:
                continue
            neighbors_checked.add(coordinates)
            status = self.get_status(*coordinates)
            if status == Status.OUT:
                continue
            elif status == opponent_color:
                neighbors_checked.add(coordinates)
            elif status == color:
                form.add(coordinates)
                if not self._is_taken(
                    *coordinates, form, neighbors_checked, color, opponent_color
                ):
                    return False
            elif status == Status.EMPTY:
                return False
        return True
