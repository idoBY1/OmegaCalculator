from abc import ABC, abstractmethod
from typing import Dict, Any, List

from src.calculatorLogic import operator


class Operator(ABC):
    """
    An abstract operator.
    """
    _priority: float
    _symbol: str

    def get_priority(self) -> float:
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
        return [op.get_end_symbol() for op in self._op_dict.values() if isinstance(op, operator.ContainerOperator)]

    def _add_op(self, op: Operator) -> None:
        """
        Assign a new operator to this object's dictionary. This method is
        intended to be used by subclasses of BaseDefinedOperators.
        :param op: The operator to add to the dictionary
        """
        if op.get_symbol() in self._op_dict.keys():  # if overloaded operator, add to a list
            if not isinstance(self._op_dict[op.get_symbol()], list):  # if list still does not exist, create it
                temp = self._op_dict[op.get_symbol()]
                self._op_dict[op.get_symbol()] = [temp]

            self._op_dict[op.get_symbol()].append(op)
        else:
            self._op_dict[op.get_symbol()] = op

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


class OmegaDefinedOperators(BaseDefinedOperators):
    """
    Defines the operators for the calculator. All the operations that can be performed by the calculator
    are provided by an instance of this class.
    """

    def __init__(self):
        self._add_op(operator.Addition())
        self._add_op(operator.Subtraction())
        self._add_op(operator.Multiplication())
        self._add_op(operator.Division())
        self._add_op(operator.Power())
        self._add_op(operator.Modulo())
        self._add_op(operator.Max())
        self._add_op(operator.Min())
        self._add_op(operator.Average())
        self._add_op(operator.Negation())
        self._add_op(operator.Factorial())
        self._add_op(operator.Brackets())
        self._add_op(operator.Minus())
        self._add_op(operator.NegativeSign())
        self._add_op(operator.SumDigits())

    def resolve_overloads(self, expression: List[str], position: int) -> Operator:
        op_symbol = expression[position]

        match op_symbol:
            case '-':
                if position <= 0: # if the first symbol, must be unary minus
                    return self._get_overloaded_by_class(op_symbol, operator.Minus)

                try:
                    prev_op = self.get_operator(expression, position - 1)
                except ValueError:
                    # previous symbol was not an operator
                    return self._get_overloaded_by_class(op_symbol, operator.Subtraction)

                if (isinstance(prev_op, operator.ContainerOperator) # if start of an independent expression
                        or isinstance(prev_op, operator.Minus)):  # or if the previous operator is unary minus
                    return self._get_overloaded_by_class(op_symbol, operator.Minus)
                elif (isinstance(prev_op, operator.BinaryOperator) # if after an operator that requires a value
                      or (isinstance(prev_op, operator.UnaryOperator)
                          and prev_op.get_operand_pos() == operator.UnaryOperator.OperandPos.AFTER)):
                    return self._get_overloaded_by_class(op_symbol, operator.NegativeSign)
                else: # default case
                    return self._get_overloaded_by_class(op_symbol, operator.Subtraction)
            case _:
                return self._op_dict[op_symbol]


