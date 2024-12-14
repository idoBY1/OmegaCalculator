from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict, List, Any

from src.calculatorLogic import calc_utils
from src.calculatorLogic.calc_errors import CalculationError, FormattingError

HIGHEST_OPERATOR_PRIORITY = 999  # All operators should have equal or lower priority from this value


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
    def get_operators_dict(self) -> Dict[str, Any]:
        """
        Get a dictionary of all the defined operators. The keys of the dictionary are
        the symbols of the Operators stored as the values. Sometimes a list will be stored as
        the value of a key and when this happens, resolve_overloads() function should be called.
        :return: The dictionary containing the pairs of strings and Operators
        """
        pass

    @abstractmethod
    def get_symbols(self):
        """
        Get all the symbols of the operators
        :return: A collection containing the symbols of all the operators.
        """
        pass

    @abstractmethod
    def get_end_symbols(self):
        """
        Get all the end symbols of the ContainerOperators.
        :return: A collection containing the end symbols of the operators
        """
        pass

    @abstractmethod
    def is_operator(self, expression: List[str], position: int) -> bool:
        """
        Returns ``True`` if the symbol at the given position is an operator and ``False`` otherwise.
        :param expression: The expression of string symbols.
        :param position: The index of the symbol at the list representing the expression.
        :return: A boolean value.
        """
        pass

    @abstractmethod
    def get_operator(self, expression: List[str], position: int) -> Operator:
        """
        Returns the operator at that position of the expression.
        :param expression: The expression of string symbols.
        :param position: The index of the operator at the list representing the expression.
        :return: The correct operator for this position.
        :raises ValueError: If the item at the given position is not an operator
        """
        pass

    @abstractmethod
    def resolve_overloads(self, expression: List[str], position: int) -> Operator:
        """
        Given a position with an overloaded operator, this function decides and returns the correct operator at this
        position in the expression. This function resolves all overloaded operators at this DefinedOperators.
        (ContainerOperators should not be overloaded!!!)
        :param expression: The expression of string symbols.
        :param position: The index of the overloaded operator at the list representing the expression.
        :return: The correct operator for this position.
        """
        pass


class BaseDefinedOperators(IDefinedOperators, ABC):
    """
    Subclasses of this class define the operators for the calculator. All the operations that can be performed by
    the calculator are defined in an instance of a subclass of this class.
    """
    _op_dict: Dict[str, Any] = {}

    def get_operators_dict(self) -> Dict[str, Any]:
        return self._op_dict

    def get_symbols(self):
        return self._op_dict.keys()

    def get_end_symbols(self):
        return [op.get_end_symbol() for op in self._op_dict.values() if isinstance(op, ContainerOperator)]

    def _add_op(self, operator: Operator) -> None:
        """
        Assign a new operator to this object's dictionary. This method is
        intended to be used by subclasses of BaseDefinedOperators.
        :param operator: The operator to add to the dictionary
        """
        if operator.get_symbol() in self._op_dict.keys():  # if overloaded operator, add to a list
            if not isinstance(self._op_dict[operator.get_symbol()], list):  # if list still does not exist, create it
                temp = self._op_dict[operator.get_symbol()]
                self._op_dict[operator.get_symbol()] = [temp]

            self._op_dict[operator.get_symbol()].append(operator)
        else:
            self._op_dict[operator.get_symbol()] = operator

    def _get_overloaded_by_class(self, op_symbol: str, op_type: type) -> Operator:
        """
        Get the desired overloaded operator from the dict.
        :param op_symbol: The key of the operator in the dictionary.
        :param op_type: The type of the operator to get.
        :return: The desired operator from this entry in the dict.
        """
        return next((op for op in self._op_dict[op_symbol] if isinstance(op, op_type)),
                    self._op_dict[op_symbol][0])

    def is_operator(self, expression: List[str], position: int) -> bool:
        return expression[position] in self._op_dict.keys()

    def get_operator(self, expression: List[str], position: int) -> Operator:
        op_symbol = expression[position]

        if not op_symbol in self._op_dict.keys():
            raise ValueError("Symbol at given position is not an operator!")

        if isinstance(self._op_dict[op_symbol], list):
            return self.resolve_overloads(expression, position)
        else:
            return self._op_dict[op_symbol]


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

    def check_position(self, expression: List[str], position: int, defined_ops: IDefinedOperators) -> None:
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

    def check_position(self, expression: List[str], position: int, defined_ops: IDefinedOperators) -> None:
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

    def check_position(self, expression: List[str], position: int, defined_ops: IDefinedOperators) -> None:
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
        self._priority = 4
        self._operand_pos = UnaryOperator.OperandPos.AFTER

    def operate(self, num: float) -> float:
        return -num

    def check_position(self, expression: List[str], position: int, defined_ops: IDefinedOperators) -> None:
        super().check_position(expression, position, defined_ops)

        for i in range(position + 1, len(expression)):
            if (calc_utils.is_float_str(expression[i])
                    or (defined_ops.is_operator(expression, i)
                        and isinstance(defined_ops.get_operator(expression, i), ContainerOperator))):
                return # only if it has a number or a container to its right
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

    def check_position(self, expression: List[str], position: int, defined_ops: IDefinedOperators) -> None:
        super().check_position(expression, position, defined_ops)

        for i in range(position + 1, len(expression)):
            if (calc_utils.is_float_str(expression[i])
                    or (defined_ops.is_operator(expression, i)
                        and isinstance(defined_ops.get_operator(expression, i), ContainerOperator))):
                return # only if it has a number or a container to its right
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
