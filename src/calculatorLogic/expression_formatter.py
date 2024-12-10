from abc import ABC, abstractmethod
from typing import Dict

from src.calculatorLogic.operator import Operator, UnaryOperator, BinaryOperator, ContainerOperator


class IFormatter(ABC):
    """
    Interface for formatting a mathematical expression from the user to a readable format for a Solver.
    """

    @abstractmethod
    def format_str(self, expression: str) -> str:
        """
        Format the string expression to a readable form by a solver.
        :param expression: Expression as string (usually from user input)
        :return: A formatted string expression
        """
        pass


class InfixToPostfixFormatter(IFormatter):
    """
    Class for converting a mathematical expression from infix to postfix notation.
    The resulting expression should be solvable by PostfixSolver.
    """

    def __init__(self, operators_dictionary: Dict[str, Operator]):
        self._op_dict = operators_dictionary

    def format_str(self, expression: str) -> str:
        pass
