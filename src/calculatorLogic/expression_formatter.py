from abc import ABC, abstractmethod
from typing import Dict, List, Any

from src.calculatorLogic import stack, operator, calc_utils
from src.calculatorLogic.operator import Operator, UnaryOperator, BinaryOperator, ContainerOperator


class IFormatter(ABC):
    """
    Interface for formatting a mathematical expression from the user to a readable format for a Solver.
    """

    @abstractmethod
    def format_expression(self, expression: List[str]) -> List[str]:
        """
        Format the string expression to a readable form by a solver.
        :param expression: Expression as a string list
        :return: A formatted string list expression
        """
        pass

    @abstractmethod
    def extract_symbols(self, expression: str) -> List[str]:
        """
        Extract the symbols from a string expression and organize them in a list.
        :param expression: Expression as string (usually from user input)
        :return: a list of math symbols
        """
        pass


class InfixToPostfixFormatter(IFormatter):
    """
    Class for converting a mathematical expression from infix to postfix notation.
    The resulting expression should be solvable by PostfixSolver.
    """

    def __init__(self, operators_dictionary: Dict[str, Operator]):
        self._op_dict = operators_dictionary

        self._op_stack = stack.ListStack()

    def extract_symbols(self, expression: str) -> List[str]:
        symbol_list = []
        temp_symbol = ""

        closing_symbols = []  # all end symbols will be stored in this list
        for op in self._op_dict.values():
            if isinstance(op, operator.ContainerOperator):
                closing_symbols.append(op.get_end_symbol())

        for ch in expression:
            if ch.isspace():
                if temp_symbol != "":
                    symbol_list.append(temp_symbol)
                    temp_symbol = ""
            elif ((temp_symbol + ch) in self._op_dict.keys()) or ((temp_symbol + ch) in closing_symbols):
                symbol_list.append(temp_symbol + ch)
                temp_symbol = ""
            elif (ch in self._op_dict.keys()) or (ch in closing_symbols):
                if temp_symbol != "":
                    symbol_list.append(temp_symbol)
                    temp_symbol = ""

                symbol_list.append(ch)
            elif calc_utils.is_float_str(temp_symbol) and not calc_utils.is_float_str(temp_symbol + ch):
                symbol_list.append(temp_symbol)
                temp_symbol = ""

                temp_symbol += ch
            else:
                temp_symbol += ch

        if temp_symbol != "":
            symbol_list.append(temp_symbol)

        return symbol_list

    # Helper function
    def correct_regualr_operator_pos(self, expression: List[str], i: int):
        # can be a binary operator only if not on first symbol and only
        # if the last symbol is not also an operator (except for unary operators that come after numbers)

        return (0 < i  # not the first in the expression
                and ((not expression[i - 1] in self._op_dict.keys())
                     or (isinstance(self._op_dict[expression[i - 1]], # last symbol wasn't an operator
                                    operator.UnaryOperator)
                         and self._op_dict[expression[i - 1]].get_operand_pos() # check for unary operator exception
                         == operator.UnaryOperator.OperandPos.BEFORE)
                     )
                )

    # Helper function
    def free_left_operators(self, left_operators: stack.IStack, postfix_expression: List[Any]):
        while ((not left_operators.is_empty()) and
               (not isinstance(self._op_dict[left_operators.top()], operator.ContainerOperator))):
            curr_op = self._op_dict[left_operators.pop()]

            if (self._op_stack.is_empty()
                    or curr_op.get_priority() > self._op_stack.top().get_priority()
                    or isinstance(self._op_stack.top(), operator.ContainerOperator)):
                self._op_stack.push(curr_op)
            else:
                while (
                        not self._op_stack.is_empty()) and curr_op.get_priority() <= self._op_stack.top().get_priority():
                    postfix_expression.append(self._op_stack.pop())

                self._op_stack.push(curr_op)

    def format_expression(self, expression: List[str]) -> List[Any]:
        self._op_stack.empty()
        postfix_expression = []

        # A dictionary storing currently opened container operators waiting to be closed.
        # Used for checking if a char is a closing char of a container.
        # This dictionary also counts the number of currently open containers of this type
        opened_containers: Dict[ContainerOperator, int] = {}

        # a list for saving the left operators and putting them after an expression
        left_operators = stack.ListStack()

        for i in range(len(expression)):
            symbol = expression[i]

            if calc_utils.is_float_str(symbol):
                try:
                    postfix_expression.append(float(symbol))
                except ValueError:
                    print(f"Error: Failed to cast '{symbol}' to a floating point value")

                self.free_left_operators(left_operators, postfix_expression)
            elif symbol in [k.get_end_symbol() for k in opened_containers.keys()]:  # if ch is a closing symbol
                while not isinstance(self._op_stack.top(), operator.ContainerOperator):  # if not reached opening symbol
                    postfix_expression.append(self._op_stack.pop())

                curr_op = self._op_stack.pop()

                postfix_expression.append(curr_op)  # add opening symbol to final expression

                opened_containers[curr_op] -= 1  # reduce opened containers count

                if opened_containers[curr_op] == 0:
                    opened_containers.pop(curr_op)

                if left_operators.pop() != curr_op.get_symbol():
                    print("Error: Incorrect container or unary operator placement")
                    return []

                self.free_left_operators(left_operators, postfix_expression)
            elif symbol in self._op_dict.keys():
                curr_op = self._op_dict[symbol]

                is_unary_left = ((isinstance(curr_op, operator.UnaryOperator)
                     and curr_op.get_operand_pos() == operator.UnaryOperator.OperandPos.AFTER))

                # check if the position of the operator is legal
                if (not isinstance(curr_op, operator.ContainerOperator)
                        and not self.correct_regualr_operator_pos(expression, i)
                        and not is_unary_left):

                    # handle a mathematical exception: only if subtraction is illegal, then this is a minus
                    if isinstance(curr_op, operator.Subtraction):
                        is_unary_left = True
                        curr_op = operator.Minus()
                    else:
                        print(f"Error: The '{curr_op.get_symbol()}' operator should only come after an operand")
                        return []

                # handle a mathematical exception: negation must come before a *number* and not any expression
                if isinstance(curr_op, operator.Negation) and (len(expression) <= i + 1 or
                                                               not (expression[i + 1].isdigit() or expression[i + 1] == '-')):
                    print("Error: Negation ({}) should only come before a number! (came before '{}')".format(
                        curr_op.get_symbol(),
                        "end-of-expression" if len(expression) <= i + 1
                        else self._op_dict[expression[i + 1]].get_symbol()))

                    return []

                if is_unary_left:
                    left_operators.push(curr_op.get_symbol())
                else:
                    # The last condition ensures that operators that come after containers will
                    # always be pushed onto the stack
                    if (self._op_stack.is_empty()
                            or curr_op.get_priority() > self._op_stack.top().get_priority()
                            or isinstance(self._op_stack.top(), operator.ContainerOperator)):
                        self._op_stack.push(curr_op)
                    else:
                        while ((not self._op_stack.is_empty()) and not self._op_stack.top() in opened_containers.keys()
                               and curr_op.get_priority() <= self._op_stack.top().get_priority()):
                            postfix_expression.append(self._op_stack.pop())

                        self._op_stack.push(curr_op)

                    # track opened containers
                    if isinstance(curr_op, operator.ContainerOperator):
                        if not curr_op in opened_containers.keys():
                            opened_containers[curr_op] = 0

                        opened_containers[curr_op] += 1

                        # a left operator should be freed only after a container that comes after it is closed
                        left_operators.push(curr_op.get_symbol())
            else:
                print(f"Error: Invalid expression, did not recognize symbol '{symbol}'")
                return []

        while not self._op_stack.is_empty():
            postfix_expression.append(self._op_stack.pop())

        return postfix_expression
