from .goban import Goban
from .position_analyzer import PositionAnalyzer
from .status import Status


class Go:
    def __init__(self, goban: Goban):
        self._goban = goban

    def get_status(self, x: int, y: int) -> Status:
        """Get the status of a given position"""
        return self._goban.get_status(x, y)

    def is_taken(self, x: int, y: int) -> bool:
        """Return True if the form at given position is surrounded"""
        analyser = PositionAnalyzer(self._goban)
        return analyser.is_taken(x, y)
