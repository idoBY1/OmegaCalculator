from abc import ABC, abstractmethod
from typing import Dict

from src.calculatorLogic.operator import Operator, UnaryOperator, BinaryOperator, ContainerOperator


class ISolver(ABC):
    """
    Interface for solving a mathematical expression.
    """

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
    """
    Class for solving mathematical expressions in postfix notation.
    """

    def __init__(self, operators_dictionary: Dict[str, Operator]):
        self._op_dict = operators_dictionary

    def solve(self, formatted_expression: str) -> float:
        pass
