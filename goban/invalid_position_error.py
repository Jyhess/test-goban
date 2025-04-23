class InvalidPositionError(ValueError):
    """Exception raised when the position is invalid."""

    def __init__(self, msg: str, x: int, y: int) -> None:
        super().__init__(msg)
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return f"{self.args[0]} at ({self.x},{self.y})"
