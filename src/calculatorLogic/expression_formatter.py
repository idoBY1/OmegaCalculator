from abc import ABC, abstractmethod
from typing import Dict

from src.calculatorLogic import stack, operator
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

        # A dictionary storing currently opened container operators waiting to be closed.
        # Used for checking if a char is a closing char of a container.
        # This dictionary also counts the number of currently open containers of this type
        self._opened_containers: Dict[ContainerOperator, int] = {}

        self._op_stack = stack.ListStack()

    def format_str(self, expression: str) -> str:
        self._op_stack.empty()
        postfix_expression = ""
        temp_op = "" # a variable to save the current operator (will sometimes be built over multiple letters)
        is_reading_num = False

        for ch in expression:
            if ch.isdigit() and temp_op == "":
                postfix_expression += ch
                is_reading_num = True
            elif ch in [k.get_end_symbol() for k in self._opened_containers.keys()]: # if ch is a closing symbol
                while not isinstance(self._op_stack.top(), operator.ContainerOperator): # if not reached opening symbol
                    postfix_expression += self._op_stack.pop().get_symbol()

                curr_op = self._op_stack.pop()

                postfix_expression += curr_op.get_symbol() # add opening symbol to final expression

                self._opened_containers[curr_op] -= 1 # reduce opened containers count

                if self._opened_containers[curr_op] == 0:
                    self._opened_containers.pop(curr_op)

            elif (temp_op + ch) in self._op_dict.keys(): # for 1 char operators "" + "x" = "x"
                curr_op = self._op_dict[temp_op + ch]

                temp_op = "" # found the operator so clean temp_op

                # The last condition ensures that operators that come after containers will
                # always be pushed onto the stack
                if (self._op_stack.is_empty()
                        or curr_op.get_priority() > self._op_stack.top().get_priority()
                        or isinstance(self._op_stack.top(), operator.ContainerOperator)):
                    self._op_stack.push(curr_op)
                else:
                    while (not self._op_stack.is_empty()) and curr_op.get_priority() <= self._op_stack.top().get_priority():
                        postfix_expression += self._op_stack.pop().get_symbol()

                    self._op_stack.push(curr_op)

                if isinstance(curr_op, operator.ContainerOperator):
                    if not curr_op in self._opened_containers.keys():
                        self._opened_containers[curr_op] = 0

                    self._opened_containers[curr_op] += 1
            elif ch.isspace():
                pass # skip whitespace characters
            else:
                # we already checked that this char is not a space or a number, so it must be a part of a
                # long operator or the expression is not valid
                temp_op += ch

            if not ch.isdigit() and is_reading_num:
                postfix_expression += " " # enter space between separate numbers
                is_reading_num = False

        if temp_op != "": # if temp_op is not empty, the input is invalid
            print("Error: invalid expression! (failed formatting)")
            return ""

        while not self._op_stack.is_empty():
            postfix_expression += self._op_stack.pop().get_symbol()

        return postfix_expression