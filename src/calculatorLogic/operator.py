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


class UnaryOperator(ABC, Operator):
    class OperandPos(Enum):
        """
        This class indicates the position of the operand relative to the
        operator. ``BEFORE`` means the operand comes before the operator, and
        ``AFTER`` means the operand comes after the operator.
        """
        BEFORE = 0
        AFTER = 1

    operand_pos: OperandPos

    @abstractmethod
    def operate(self, num: float) -> float:
        """
        Perform the operation on the number and return a result.
        :param num: A floating point number to perform the operation with
        :return: The result of the operation as a floating point number
        """
        pass
