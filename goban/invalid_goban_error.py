class InvalidGobanError(ValueError):
    """Exception raised when the goban is invalid."""

    def __init__(self, msg: str, line: str, line_index: int) -> None:
        super().__init__(msg)
        self.line = line
        self.line_index = line_index

    def __str__(self) -> str:
        if self.line_index < 0:
            return str(self.args[0])
        return f"{self.args[0]} at line {self.line_index}: {self.line:.10}"
