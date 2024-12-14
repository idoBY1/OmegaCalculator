class CalculationError(Exception):
    """
    Exception raised for errors occurring mid-calculation of an expression.
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class FormattingError(Exception):
    """
    Exception raised for errors occurring while formatting an expression.
    """

    def __init__(self, message, position: int = -1):
        self.message = message
        self.position = position
        super().__init__(self.message)


class SolvingError(Exception):
    """
    Exception raised for errors occurring while solving an expression.
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
