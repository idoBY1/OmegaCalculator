from abc import ABC, abstractmethod
from typing import Dict, List, Any, Tuple

from src.calculatorLogic import stack, operator
from src.calculatorLogic.calc_errors import SolvingError
from src.calculatorLogic.operator import Operator, UnaryOperator, BinaryOperator, ContainerOperator

ROUNDING_DIGITS = 12

class ISolver(ABC):
    """
    Interface for solving a mathematical expression.
    """

    @abstractmethod
    def solve(self, formatted_expression: List[Any]) -> float:
        """
        Solve the given expression and return a numerical answer
        as a floating point number.
        :param formatted_expression: The formatted mathematical expression to be solved as a list.
        :return: A floating point number representing the answer to the mathematical expression.
        :raises SolvingError: If an error occurred while solving the mathematical expression.
        """
        pass


class PostfixSolver(ISolver):
    """
    Class for solving mathematical expressions in postfix notation.
    """

    def solve(self, formatted_expression: List[Any]) -> float:
        operand_stack = stack.ListStack()

        for symbol in formatted_expression:
            if isinstance(symbol, float):
                operand_stack.push(symbol)
            elif isinstance(symbol, operator.Operator):
                if isinstance(symbol, operator.BinaryOperator):
                    try:
                        # reverse order because of stack (LIFO)
                        num2 = operand_stack.pop()
                        num1 = operand_stack.pop()

                        result = symbol.operate(num1, num2)

                        operand_stack.push(result)
                    except IndexError:
                        raise SolvingError(f"Error: Not enough operands for {str(symbol)}")
                    except operator.CalculationError as e:
                        raise SolvingError(f"Error: {e.message}")
                elif isinstance(symbol, (operator.UnaryOperator, operator.ContainerOperator)):
                    try:
                        num1 = operand_stack.pop()
                        result = symbol.operate(num1)

                        operand_stack.push(result)
                    except IndexError:
                        raise SolvingError(f"Error: Not enough operands for {str(symbol)}")
                    except operator.CalculationError as e:
                        raise SolvingError(f"Error: {e.message}")
                else:
                    raise SolvingError(f"Error: Does not recognise the operator {str(symbol)}")
            else:
                raise SolvingError(f"Error: Does not recognise {str(symbol)}")

        if len(operand_stack) > 1:
            raise SolvingError(f"Error: Too many operands! (each operand should be tied to the expression by some operator)")

        if operand_stack.is_empty():
            raise SolvingError(f"Error: Empty expression!")

        result = operand_stack.pop()

        # round the result number to avoid floating point operations errors
        return round(result, ROUNDING_DIGITS)