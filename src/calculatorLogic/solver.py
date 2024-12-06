from abc import ABC, abstractmethod


class ISolver(ABC):
    @abstractmethod
    def solve(self, formatted_expression: str) -> float:
        """
        Solve the given expression and return a numerical answer
        as a floating point number.
        :param formatted_expression: The formatted mathematical expression to be solved as a string
        :return: A floating point number representing the answer to the mathematical expression
        """
        pass

class PostfixSolver(ISolver):
    def solve(self, formatted_expression: str) -> float:
        pass