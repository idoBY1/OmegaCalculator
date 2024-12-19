import math
from abc import abstractmethod
from enum import Enum
from typing import List

from src.calculatorLogic import calc_utils, defined_operators
from src.calculatorLogic.calc_errors import CalculationError, FormattingError
from src.calculatorLogic.defined_operators import Operator

HIGHEST_OPERATOR_PRIORITY = 999  # All operators should have equal or lower priority from this value

MAX_ITER = 100000 # The max amount of full iterations allowed for the calculator to perform on a single operation

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

    def check_position(self, expression: List[str], position: int,
                       defined_ops: defined_operators.IDefinedOperators) -> None:
        """
        Checks if the given position is legal for this operator. raises an exception if the position
        is illegal for the operator.
        :param expression: The expression as string list before formatting.
        :param position: The position in the expression.
        :param defined_ops: The object containing the defined operators.
        :raises FormattingError: If the position is illegal
        """
        if self._operand_pos == UnaryOperator.OperandPos.BEFORE:
            if position < 1:
                raise FormattingError(f"Error: Missing a value before '{self._symbol}'", position)

            if defined_ops.is_operator(expression, position - 1):
                prev_op = defined_ops.get_operator(expression, position - 1)

                if isinstance(prev_op, UnaryOperator) and prev_op.get_operand_pos() == UnaryOperator.OperandPos.BEFORE:
                    return
                elif isinstance(prev_op, ContainerOperator):
                    raise FormattingError(f"Error: Missing a value before '{self._symbol}'", position)
                else:
                    raise FormattingError(f"Error: '{self._symbol}' cannot come after an operator", position)
        else:
            if not position < len(expression) - 1:
                raise FormattingError(f"Error: Missing a value after '{self._symbol}'")

            if expression[position + 1] in defined_ops.get_end_symbols():
                raise FormattingError(f"Error: Missing a value after '{self._symbol}'", position)


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

    def check_position(self, expression: List[str], position: int,
                       defined_ops: defined_operators.IDefinedOperators) -> None:
        """
        Checks if the given position is legal for this operator. raises an exception if the position
        is illegal for the operator.
        :param expression: The expression as string list before formatting.
        :param position: The position in the expression.
        :param defined_ops: The object containing the defined operators.
        :raises FormattingError: If the position is illegal
        """
        if position < 1:
            raise FormattingError(f"Error: Missing a value before '{self._symbol}'", position)

        if defined_ops.is_operator(expression, position - 1):
            prev_op = defined_ops.get_operator(expression, position - 1)

            if isinstance(prev_op, UnaryOperator) and prev_op.get_operand_pos() == UnaryOperator.OperandPos.BEFORE:
                return
            elif isinstance(prev_op, ContainerOperator):
                raise FormattingError(f"Error: Missing a value before '{self._symbol}'", position)
            else:
                raise FormattingError(f"Error: '{self._symbol}' cannot come after an operator", position)

        if not position < len(expression) - 1:
            raise FormattingError(f"Error: Missing a value after '{self._symbol}'")

        if expression[position + 1] in defined_ops.get_end_symbols():
            raise FormattingError(f"Error: Missing a value after '{self._symbol}'", position)


class ContainerOperator(Operator):
    """
    An operator that operates on a defined and enclosed part of an expression.

    Examples: brackets(())
    (could be used for other purposes like implementing sin(x) or other functions)
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
            raise CalculationError("Error: Cannot divide by zero")

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
        if num1 < 0 and -1 < num2 < 1:
            raise CalculationError(f"Error: Cannot raise a negative number to a fraction's power ({num1}^{num2} = ???)")

        if num1 == 0 and num2 < 0:
            raise CalculationError(f"Error: Cannot raise zero to a negative number's power ({num1}^{num2} = ???)")

        if num1 == 0 and num2 == 0:
            raise CalculationError(f"Error: Cannot raise zero to the power of zero ({num1}^{num2} = ???)")

        try:
            return math.pow(num1, num2)
        except OverflowError:
            raise CalculationError(f"Error: The result of {num1}^{num2} is too large")


class Modulo(BinaryOperator):
    """
    The binary operator for modulo.

    Symbol: '%'

    In an expression: a % b
    """

    def __init__(self):
        self._symbol = '%'
        self._priority = 4

    def operate(self, num1: float, num2: float) -> float:
        if num2 == 0:
            raise CalculationError(f"Error: Cannot perform modulo by zero ({num1} % 0 = ???)")

        return num1 % num2


class Max(BinaryOperator):
    """
    The binary operator for the maximum of two numbers.

    Symbol: '$'

    In an expression: a $ b
    """

    def __init__(self):
        self._symbol = '$'
        self._priority = 5

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
        self._priority = 5

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
        self._priority = 5

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
        self._priority = 6
        self._operand_pos = UnaryOperator.OperandPos.AFTER

    def operate(self, num: float) -> float:
        return -num

    def check_position(self, expression: List[str], position: int,
                       defined_ops: defined_operators.IDefinedOperators) -> None:
        super().check_position(expression, position, defined_ops)

        for i in range(position + 1, len(expression)):
            if calc_utils.is_float_str(expression[i]):
                return
            elif not expression[i] == '-':
                raise FormattingError(f"Error: '{self._symbol}' cannot come before '{expression[i]}'", i)

        raise FormattingError(f"Error: Missing a value after '{self._symbol}'", position)


class Minus(UnaryOperator):
    """
    The unary operator for flipping a number's sign (lower priority).

    Symbol: '-'

    In an expression: -x
    """

    def __init__(self):
        self._symbol = "-"
        self._priority = 3.5
        self._operand_pos = UnaryOperator.OperandPos.AFTER

    def operate(self, num: float) -> float:
        return -num

    def check_position(self, expression: List[str], position: int,
                       defined_ops: defined_operators.IDefinedOperators) -> None:
        super().check_position(expression, position, defined_ops)

        for i in range(position + 1, len(expression)):
            if (calc_utils.is_float_str(expression[i])
                    or (defined_ops.is_operator(expression, i)
                        and isinstance(defined_ops.get_operator(expression, i), ContainerOperator))):
                return  # only if it has a number or a container to its right
            elif not expression[i] == '-':
                raise FormattingError(f"Error: '{self._symbol}' cannot come before '{expression[i]}'", i)

        raise FormattingError(f"Error: Missing a value after '{self._symbol}'", position)

    def __str__(self) -> str:
        return self._symbol + " (unary minus)"


class NegativeSign(UnaryOperator):
    """
    The unary operator for flipping a number's sign.

    Symbol: '-'

    In an expression: -x
    """

    def __init__(self):
        self._symbol = "-"
        self._priority = 10
        self._operand_pos = UnaryOperator.OperandPos.AFTER

    def operate(self, num: float) -> float:
        return -num

    def check_position(self, expression: List[str], position: int,
                       defined_ops: defined_operators.IDefinedOperators) -> None:
        super().check_position(expression, position, defined_ops)

        for i in range(position + 1, len(expression)):
            if (calc_utils.is_float_str(expression[i])
                    or (defined_ops.is_operator(expression, i)
                        and isinstance(defined_ops.get_operator(expression, i), ContainerOperator))):
                return  # only if it has a number or a container to its right
            elif not expression[i] == '-':
                raise FormattingError(f"Error: '{self._symbol}' cannot come before '{expression[i]}'", i)

        raise FormattingError(f"Error: Missing a value after '{self._symbol}'", position)

    def __str__(self) -> str:
        return self._symbol + " (sign)"


class Factorial(UnaryOperator):
    """
    The unary operator for factorial.

    Symbol: '!'

    In an expression: x!
    """

    def __init__(self):
        self._symbol = '!'
        self._priority = 6
        self._operand_pos = UnaryOperator.OperandPos.BEFORE

    def operate(self, num: float) -> float:
        if num < 0:
            raise CalculationError(f"Error: Cannot calculate the factorial of a negative number ({num}! = ???)")

        if num % 1 != 0:
            raise CalculationError(f"Error: Can only calculate the factorial of a whole number ({num}! = ???)")

        res = 1.0

        # if the amount of iterations is bigger than the max of allowed iterations, raise an error
        if round(num) + 1 > MAX_ITER:
            raise CalculationError(f"Error: The result of {num}! is too large")

        for i in range(1, round(num) + 1):
            res *= i

        return res


class SumDigits(UnaryOperator):
    """
    The unary operator for summing the digits of a number.

    Symbol: '#'

    In an expression: x#
    """

    # avoids subtle bugs involving floating point precision
    MAX_NUMBER_DIGITS = 12
    ROUNDING_DIGITS = 14

    def __init__(self):
        self._symbol = '#'
        self._priority = 6
        self._operand_pos = UnaryOperator.OperandPos.BEFORE

    def operate(self, num: float) -> float:
        if num < 0:
            raise CalculationError(f"Error: Cannot calculate the sum of digits of a negative number ({num}# = ???)")

        str_num = format(num, f".{SumDigits.ROUNDING_DIGITS}g")
        str_num = str_num.lower().split("e", 1)[0] # remove exponent

        if len(str_num) > SumDigits.MAX_NUMBER_DIGITS:
            raise CalculationError(f"Error: Cannot calculate sum of digits for a number with "
                                   f"too many digits (loss of precision)")

        digits_sum = 0
        for str_digit in str_num:
            if str_digit.isdigit():
                digits_sum += float(str_digit)

        return digits_sum


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
