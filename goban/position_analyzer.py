from typing import Iterable

from .goban import Goban
from .invalid_position_error import InvalidPositionError
from .status import Status


class PositionAnalyzer:
    def __init__(self, goban: Goban, x: int, y: int) -> None:
        self._goban = goban
        status = self._goban.get_status(x, y)
        if status == Status.OUT:
            raise InvalidPositionError("Position is out of goban", x, y)
        self._coordinates = (x, y)
        self._color = status
        self._opponent_color = (
            Status.WHITE if self._color == Status.BLACK else Status.BLACK
        )
        self._form: set[tuple[int, int]] = set()
        self._neighbors_checked: set[tuple[int, int]] = set()

    def is_empty(self) -> bool:
        """Return True if there is no stone at given position"""
        return self._goban.get_status(*self._coordinates) == Status.EMPTY

    def is_taken(self) -> bool:
        """Return True if the form at given position is surrounded"""
        if self.is_empty():
            raise InvalidPositionError("Position is empty", *self._coordinates)
        return self._is_taken(self._coordinates)

    def _is_taken(
        self,
        coordinates: tuple[int, int],
    ) -> bool:
        self._form.add(coordinates)
        for neighbors in self._all_new_neighbors(coordinates):
            status = self._goban.get_status(*neighbors)
            if status == Status.EMPTY:
                # Found a liberty, stone is free :)
                return False
            elif status == self._color:
                if not self._is_taken(neighbors):
                    # Found a liberty in the rest of the form, stone is free :)
                    return False
                # This direction is not a free form, check next direction
            elif status == self._opponent_color:
                # No liberty with opponent, check next direction
                self._neighbors_checked.add(neighbors)
            elif status == Status.OUT:
                # No liberty on border, check next direction
                continue
        # Stone is surrounded
        return True

    def _all_new_neighbors(
        self, coordinates: tuple[int, int]
    ) -> Iterable[tuple[int, int]]:
        for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            neighbors = (coordinates[0] + dx, coordinates[1] + dy)
            if self._already_analyzed(neighbors):
                continue
            yield neighbors

    def _already_analyzed(self, coordinates: tuple[int, int]) -> bool:
        return coordinates in self._form or coordinates in self._neighbors_checked
