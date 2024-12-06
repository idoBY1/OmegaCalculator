import math
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum

@dataclass
class Operator(ABC):
    _priority: int
    _symbol: str

    def get_priority(self) -> int:
        """
        Get the priority of the operator in the order of operations.
        :return: The number representing the priority of the operation (higher number
            indicates higher priority).
        """
        return self._priority

    def get_symbol(self) -> str:
        """
        Get the symbol representing the operation in a math expression.
        :return: The symbol as a string
        """
        return self._symbol


class UnaryOperator(Operator):
    class OperandPos(Enum):
        """
        This class indicates the position of the operand relative to the
        operator. ``BEFORE`` means the operand comes before the operator, and
        ``AFTER`` means the operand comes after the operator.
        """
        BEFORE = 0
        AFTER = 1

    _operand_pos: OperandPos

    @abstractmethod
    def operate(self, num: float) -> float:
        """
        Perform the operation on the number and return a result.
        :param num: A floating point number to perform the operation with
        :return: The result of the operation as a floating point number
        """
        pass


class BinaryOperator(Operator):
    @abstractmethod
    def operate(self, num1: float, num2: float) -> float:
        """
        Perform the operation on the numbers and return a result.
        :param num1: The first floating point number to perform the operation with
        :param num2: The second floating point number to perform the operation with
        :return: The result of the operation as a floating point number
        """
        pass


# The actual operators are implemented here
class Addition(BinaryOperator):
    def __init__(self):
        self._symbol = '+'
        self._priority = 1

    def operate(self, num1: float, num2: float) -> float:
        return num1 + num2


class Subtraction(BinaryOperator):
    def __init__(self):
        self._symbol = '-'
        self._priority = 1

    def operate(self, num1: float, num2: float) -> float:
        return num1 - num2


class Multiplication(BinaryOperator):
    def __init__(self):
        self._symbol = '*'
        self._priority = 2

    def operate(self, num1: float, num2: float) -> float:
        return num1 * num2


class Division(BinaryOperator):
    def __init__(self):
        self._symbol = '/'
        self._priority = 2

    def operate(self, num1: float, num2: float) -> float:
        return num1 / num2


class Power(BinaryOperator):
    def __init__(self):
        self._symbol = '^'
        self._priority = 3

    def operate(self, num1: float, num2: float) -> float:
        return num1 ** num2


class Modulo(BinaryOperator):
    def __init__(self):
        self._symbol = '%'
        self._priority = 4

    def operate(self, num1: float, num2: float) -> float:
        return num1 % num2


class Max(BinaryOperator):
    def __init__(self):
        self._symbol = '$'
        self._priority = 5

    def operate(self, num1: float, num2: float) -> float:
        return num1 if num1 > num2 else num2


class Min(BinaryOperator):
    def __init__(self):
        self._symbol = '&'
        self._priority = 5

    def operate(self, num1: float, num2: float) -> float:
        return num1 if num1 < num2 else num2


class Average(BinaryOperator):
    def __init__(self):
        self._symbol = '@'
        self._priority = 5

    def operate(self, num1: float, num2: float) -> float:
        return (num1 + num2) / 2.0


class Negation(UnaryOperator):
    def __init__(self):
        self._symbol = '~'
        self._priority = 6
        self._operand_pos = UnaryOperator.OperandPos.AFTER

    def operate(self, num: float) -> float:
        return -num


class Factorial(UnaryOperator):
    def __init__(self):
        self._symbol = '!'
        self._priority = 6
        self._operand_pos = UnaryOperator.OperandPos.BEFORE

    def operate(self, num: float) -> float:
        try:
            return math.gamma(num + 1) # extension of factorial to real numbers
        except ValueError:
            print("Cannot compute factorial of " + str(num) + "!")