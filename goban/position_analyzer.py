from typing import Iterable

from .goban import Goban
from .invalid_position_error import InvalidPositionError
from .status import Status


class PositionAnalyzer:
    def __init__(self, goban: Goban) -> None:
        self._goban = goban

    def is_taken(self, x: int, y: int) -> bool:
        status = self._goban.get_status(x, y)
        if status == Status.EMPTY:
            raise InvalidPositionError("Position is empty", x, y)
        if status == Status.OUT:
            raise InvalidPositionError("Position is out of goban", x, y)

        color = status
        start_coordinates = (x, y)
        positions_to_check = [start_coordinates]
        already_checked_positions = {start_coordinates}

        def unchecked_positions_generator() -> Iterable[tuple[int, int]]:
            while positions_to_check:
                position_to_check = positions_to_check.pop()
                for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                    neighbor = (position_to_check[0] + dx, position_to_check[1] + dy)
                    if neighbor in already_checked_positions:
                        continue
                    yield neighbor

        for position in unchecked_positions_generator():
            already_checked_positions.add(position)
            status = self._goban.get_status(*position)
            if status == Status.EMPTY:
                # Found a liberty, stone is free :)
                return False
            elif status == color:
                # Form continue, will check this position
                positions_to_check.append(position)
            else:
                # Found an opponent stone or a border, continue searching for liberty
                continue
        return True
