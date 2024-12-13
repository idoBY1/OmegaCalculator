from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict

HIGHEST_OPERATOR_PRIORITY = 999 # All operators should have equal or lower priority from this value

class Operator(ABC):
    """
    An abstract operator.
    """
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

    def __str__(self) -> str:
        return self._symbol


class IDefinedOperators(ABC):
    """
    A class that implements this interface will provide the operators for the calculator.
    """

    @abstractmethod
    def get_operators_dict(self) -> Dict[str, Operator]:
        """
        Get a dictionary of all the defined operators. The keys of the dictionary are
        the symbols of the Operators stored as the values.
        :return: The dictionary containing the pairs of strings and Operators
        """
        pass


class BaseDefinedOperators(IDefinedOperators, ABC):
    """
    Subclasses of this class define the operators for the calculator. All the operations that can be performed by
    the calculator are defined in the dictionary provided by an instance of a subclass of this class.
    """
    _op_dict: Dict[str, Operator] = {}

    def get_operators_dict(self) -> Dict[str, Operator]:
        return self._op_dict

    def _add_op(self, operator: Operator) -> bool:
        """
        Assign a new operator to this object's dictionary. This method is
        intended to be used by subclasses of BaseDefinedOperators.
        :param operator: The operator to add to the dictionary
        :return: ``True`` if the operator was successfully added to the dictionary and ``False`` if
            the dictionary already contained an operator with this symbol
        """
        if operator.get_symbol() in self._op_dict.keys():
            return False

        self._op_dict[operator.get_symbol()] = operator

        return True


class CalculationError(Exception):
    """
    Exception raised for errors occurring mid-calculation of an expression.
    """


    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


# Subclasses of Operator
class UnaryOperator(Operator):
    """
    An operator that operates on a single value.

    Examples: factorial(!), negation(~)
    """

    class OperandPos(Enum):
        """
        This class indicates the position of the operand relative to the
        operator. ``BEFORE`` means the operand comes before the operator, and
        ``AFTER`` means the operand comes after the operator.
        """
        BEFORE = 0
        AFTER = 1

    _operand_pos: OperandPos

    def get_operand_pos(self):
        return self._operand_pos

    @abstractmethod
    def operate(self, num: float) -> float:
        """
        Perform the operation on the number and return a result.
        :param num: A floating point number to perform the operation with
        :return: The result of the operation as a floating point number
        :raises CalculationError: If the operation failed because of its calculation
        """
        pass


class BinaryOperator(Operator):
    """
    An operator that operates on two values and returns one.

    Examples: addition(+), division(/)
    """

    @abstractmethod
    def operate(self, num1: float, num2: float) -> float:
        """
        Perform the operation on the numbers and return a result.
        :param num1: The first floating point number to perform the operation with
        :param num2: The second floating point number to perform the operation with
        :return: The result of the operation as a floating point number
        :raises CalculationError: If the operation failed because of its calculation
        """
        pass

class ContainerOperator(Operator):
    """
    An operator that operates on a defined and enclosed part of an expression.

    Examples: brackets(())
    (could be used for other purposes like implementing sin(x) or |x|)
    """
    _end_symbol: str

    def get_end_symbol(self):
        """
        Get the symbol representing the end of the operation in a math expression.
        :return: The symbol as a string
        """
        return self._end_symbol

    @abstractmethod
    def operate(self, num: float) -> float:
        """
        Perform the operation on the number and return a result.
        :param num: A floating point number to perform the operation with
        :return: The result of the operation as a floating point number
        :raises CalculationError: If the operation failed because of its calculation
        """
        pass


# The actual operators are implemented here
class Addition(BinaryOperator):
    """
    The binary operator for addition.

    Symbol: '+'

    In an expression: a + b
    """

    def __init__(self):
        self._symbol = '+'
        self._priority = 1

    def operate(self, num1: float, num2: float) -> float:
        return num1 + num2


class Subtraction(BinaryOperator):
    """
    The binary operator for subtraction.

    Symbol: '-'

    In an expression: a - b
    """

    def __init__(self):
        self._symbol = '-'
        self._priority = 1

    def operate(self, num1: float, num2: float) -> float:
        return num1 - num2


class Multiplication(BinaryOperator):
    """
    The binary operator for multiplication.

    Symbol: '*'

    In an expression: a * b
    """

    def __init__(self):
        self._symbol = '*'
        self._priority = 2

    def operate(self, num1: float, num2: float) -> float:
        return num1 * num2


class Division(BinaryOperator):
    """
    The binary operator for division.

    Symbol: '/'

    In an expression: a / b
    """

    def __init__(self):
        self._symbol = '/'
        self._priority = 2

    def operate(self, num1: float, num2: float) -> float:
        if num2 == 0:
            raise CalculationError("Cannot divide by zero")

        return num1 / num2


class Power(BinaryOperator):
    """
    The binary operator for power.

    Symbol: '^'

    In an expression: a ^ b
    """

    def __init__(self):
        self._symbol = '^'
        self._priority = 3

    def operate(self, num1: float, num2: float) -> float:
        return num1 ** num2


class Modulo(BinaryOperator):
    """
    The binary operator for modulo.

    Symbol: '%'

    In an expression: a % b
    """

    def __init__(self):
        self._symbol = '%'
        self._priority = 5

    def operate(self, num1: float, num2: float) -> float:
        return num1 % num2


class Max(BinaryOperator):
    """
    The binary operator for the maximum of two numbers.

    Symbol: '$'

    In an expression: a $ b
    """

    def __init__(self):
        self._symbol = '$'
        self._priority = 6

    def operate(self, num1: float, num2: float) -> float:
        return num1 if num1 > num2 else num2


class Min(BinaryOperator):
    """
    The binary operator for the minimum of two numbers.

    Symbol: '&'

    In an expression: a & b
    """

    def __init__(self):
        self._symbol = '&'
        self._priority = 6

    def operate(self, num1: float, num2: float) -> float:
        return num1 if num1 < num2 else num2


class Average(BinaryOperator):
    """
    The binary operator for the average of two numbers.

    Symbol: '@'

    In an expression: a @ b
    """

    def __init__(self):
        self._symbol = '@'
        self._priority = 6

    def operate(self, num1: float, num2: float) -> float:
        return (num1 + num2) / 2.0


class Negation(UnaryOperator):
    """
    The unary operator for negation.

    Symbol: '~'

    In an expression: ~x
    """

    def __init__(self):
        self._symbol = '~'
        self._priority = 7
        self._operand_pos = UnaryOperator.OperandPos.AFTER

    def operate(self, num: float) -> float:
        return -num

class Minus(UnaryOperator):
    """
    The unary operator for flipping a numbers sign.

    Symbol: '-_'

    In an expression: -x
    """

    def __init__(self):
        self._symbol = "-_"
        self._priority = 10
        self._operand_pos = UnaryOperator.OperandPos.AFTER

    def operate(self, num: float) -> float:
        return -num

class Factorial(UnaryOperator):
    """
    The unary operator for factorial.

    Symbol: '!'

    In an expression: x!
    """

    def __init__(self):
        self._symbol = '!'
        self._priority = 7
        self._operand_pos = UnaryOperator.OperandPos.BEFORE

    def operate(self, num: float) -> float:
        if num < 0:
            raise CalculationError(f"Cannot calculate the factorial of a negative number ({num}! = ???)")

        if num % 1 != 0:
            raise CalculationError(f"Can only calculate the factorial of a whole number ({num}! = ???)")

        res = 1.0

        for i in range(1, round(num) + 1):
            res *= i

        return res


class Brackets(ContainerOperator):
    """
    The container operator for brackets.

    Symbol: '('

    End symbol: ')'

    In an expression: (x)
    """

    def __init__(self):
        self._symbol = '('
        self._end_symbol = ')'
        self._priority = HIGHEST_OPERATOR_PRIORITY  # brackets will always have the highest priority

    def operate(self, num: float) -> float:
        return num  # brackets do not change the value given to them
