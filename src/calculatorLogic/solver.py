from abc import ABC, abstractmethod
from typing import Dict, List, Any, Tuple

from src.calculatorLogic import stack, operator
from src.calculatorLogic.operator import Operator, UnaryOperator, BinaryOperator, ContainerOperator

ROUNDING_DIGITS = 12

class ISolver(ABC):
    """
    Interface for solving a mathematical expression.
    """

    @abstractmethod
    def solve(self, formatted_expression: List[Any]) -> Tuple[bool, float]:
        """
        Solve the given expression and return a numerical answer
        as a floating point number.
        :param formatted_expression: The formatted mathematical expression to be solved as a list
        :return: A tuple containing a bool indicating if the function succeeded and a
         floating point number representing the answer to the mathematical expression if the function succeeded
        """
        pass


class PostfixSolver(ISolver):
    """
    Class for solving mathematical expressions in postfix notation.
    """

    def solve(self, formatted_expression: List[Any]) -> Tuple[bool, float]:
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
                        print(f"Error: Not enough operands for {str(symbol)}")
                        return False, 0
                    except operator.CalculationError as e:
                        print(f"Error: {e.message}")
                        return False, 0
                elif isinstance(symbol, (operator.UnaryOperator, operator.ContainerOperator)):
                    try:
                        num1 = operand_stack.pop()
                        result = symbol.operate(num1)

                        operand_stack.push(result)
                    except IndexError:
                        print(f"Error: Not enough operands for {str(symbol)}")
                        return False, 0
                    except operator.CalculationError as e:
                        print(f"Error: {e.message}")
                        return False, 0
                else:
                    print(f"Error: Does not recognise the operator {str(symbol)}")
                    return False, 0
            else:
                print(f"Error: Does not recognise {str(symbol)}")
                return False, 0

        if len(operand_stack) > 1:
            print(f"Error: Too many operands! (each operand should be tied to the expression by some operator)")
            return False, 0

        if operand_stack.is_empty():
            print(f"Error: Empty expression!")
            return False, 0

        result = operand_stack.pop()

        # round the result number to avoid floating point operations errors
        return True, round(result, ROUNDING_DIGITS)