from abc import ABC, abstractmethod
from typing import Dict, List, Any

from src.calculatorLogic import stack, operator, calc_utils, defined_operators
from src.calculatorLogic.calc_errors import FormattingError
from src.calculatorLogic.calc_utils import organize_whitespace


class IFormatter(ABC):
    """
    Interface for formatting a mathematical expression from the user to a readable format for a Solver.
    """

    @abstractmethod
    def format_expression(self, expression: List[str]) -> List[Any]:
        """
        Format the string expression to a readable form by a solver.
        :param expression: Expression as a string list
        :return: A formatted symbol list expression
        :raises FormattingError: If an error occurred while formatting the expression.
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

    def __init__(self, defined_ops: defined_operators.IDefinedOperators):
        self._defined_ops = defined_ops

        self._op_stack = stack.ListStack() # stack for storing operators before inserting them in an expression
        self._left_operators = stack.ListStack() # stack for storing the left-operators (they behave a bit differently)

    def extract_symbols(self, expression: str) -> List[str]:
        symbol_list = []
        temp_symbol = ""

        expression = organize_whitespace(expression)  # delete repeats of spaces

        closing_symbols = self._defined_ops.get_end_symbols()

        for i in range(len(expression)):
            ch = expression[i]

            if ch.isspace():
                if (temp_symbol != ""
                        and not calc_utils.is_float_str(temp_symbol)): # make sure to only separate if not a number
                    symbol_list.append(temp_symbol)
                    temp_symbol = ""
            elif ((temp_symbol + ch) in self._defined_ops.get_symbols()) or ((temp_symbol + ch) in closing_symbols):
                # if this temp_symbol creates with this char a defined operator

                symbol_list.append(temp_symbol + ch)
                temp_symbol = ""
            elif (ch in self._defined_ops.get_symbols()) or (ch in closing_symbols):
                # if this char alone creates a defined operator

                if temp_symbol != "":
                    symbol_list.append(temp_symbol)
                    temp_symbol = ""

                symbol_list.append(ch)
            elif calc_utils.is_float_str(temp_symbol) and not calc_utils.is_float_str(temp_symbol + ch):
                # if at the end of a valid number

                symbol_list.append(temp_symbol)
                temp_symbol = ""

                temp_symbol += ch
            else:
                temp_symbol += ch

        if temp_symbol != "":
            symbol_list.append(temp_symbol)

        return symbol_list

    # helper function
    def insert_operator(self, op: operator.Operator, postfix_expression: List[Any],
                        opened_containers: Dict[operator.ContainerOperator, int]):
        # if operator is a left unary operator, push to left_operators without performing any checks for now
        if (isinstance(op, operator.UnaryOperator)
                and op.get_operand_pos() == operator.UnaryOperator.OperandPos.AFTER):
            self._left_operators.push(op)
        else:
            if ((self._op_stack.is_empty()
                 or op.get_priority() > self._op_stack.top().get_priority()
                 or isinstance(self._op_stack.top(),
                               operator.ContainerOperator))  # ignore priority at the start of a container
                    and (self._left_operators.is_empty()
                         or op.get_priority() > self._left_operators.top().get_priority()
                         or isinstance(self._left_operators.top(), operator.ContainerOperator))):
                # if the operator has higher priority than everything else already pushed
                self._op_stack.push(op)
            else:
                # while the current operator has less priority than the top of the stack
                while ((not self._op_stack.is_empty())
                       and op.get_priority() <= self._op_stack.top().get_priority()
                       and not isinstance(self._op_stack.top(), operator.ContainerOperator)):

                    # if the current top left-operator has the highest priority
                    if ((not self._left_operators.is_empty()) and self._left_operators.top().get_priority()
                            >= self._op_stack.top().get_priority()
                            and not isinstance(self._left_operators.top(), operator.ContainerOperator)):
                        postfix_expression.append(self._left_operators.pop())
                    else:
                        # if the current regular operator at the top of the stack has the highest priority
                        postfix_expression.append(self._op_stack.pop())

                # check for the case that all regular operators have less priority than the current operator but
                # the left-operators have more priority the current operator
                while ((not self._left_operators.is_empty())
                       and self._left_operators.top().get_priority() >= op.get_priority()
                       and not isinstance(self._left_operators.top(), operator.ContainerOperator)):
                    postfix_expression.append(self._left_operators.pop())

                # after all for the operators with higher priority have been inserted to the final expression
                self._op_stack.push(op)

            # track opened containers
            # counts the number of closing symbols that should appear later
            if isinstance(op, operator.ContainerOperator):
                if not op in opened_containers.keys():
                    opened_containers[op] = 0

                opened_containers[op] += 1
                self._left_operators.push(op)

    # helper function
    def free_until_start_of_container(self, postfix_expression: List[Any]):
        # while not reached opening symbol
        while not isinstance(self._op_stack.top(), operator.ContainerOperator):
            # if there is a left-operator with higher priority
            if (self._left_operators.top().get_priority() >= self._op_stack.top().get_priority()
                    and not isinstance(self._left_operators.top(), operator.ContainerOperator)):
                postfix_expression.append(self._left_operators.pop())

            postfix_expression.append(self._op_stack.pop())

        # if all regular operators have been freed but there are still left-operators before the container symbol
        while not isinstance(self._left_operators.top(), operator.ContainerOperator):
            postfix_expression.append(self._left_operators.pop())

    def format_expression(self, expression: List[str]) -> List[Any]:
        self._op_stack.empty()
        self._left_operators.empty()
        postfix_expression = []

        # A dictionary storing currently opened container operators waiting to be closed.
        # Used for checking if a char is a closing char of a container.
        # This dictionary also counts the number of currently open containers of this type
        opened_containers: Dict[operator.ContainerOperator, int] = {}

        for i in range(len(expression)):
            symbol = expression[i]

            if calc_utils.is_float_str(symbol):
                try:
                    postfix_expression.append(float(symbol))
                except ValueError:
                    raise FormattingError(f"Error: Failed to cast '{symbol}' to a floating point value", i)
            elif symbol in [k.get_end_symbol() for k in opened_containers.keys()]: # if symbol is a closing symbol
                self.free_until_start_of_container(postfix_expression)

                curr_op = self._op_stack.pop() # pop the container symbol form the stack
                postfix_expression.append(curr_op) # add the container symbol to final expression

                opened_containers[curr_op] -= 1  # reduce opened containers count
                self._left_operators.pop() # also pop the container symbol from the left operators stack

                # if the count of this container reached 0, delete it from the dictionary
                if opened_containers[curr_op] == 0:
                    opened_containers.pop(curr_op)
            elif symbol in self._defined_ops.get_symbols(): # if symbol is an operator
                curr_op = self._defined_ops.get_operator(expression, i)

                # should throw an exception if the operator is in an illegal position
                if isinstance(curr_op, (operator.UnaryOperator, operator.BinaryOperator)):
                    curr_op.check_position(expression, i, self._defined_ops)

                self.insert_operator(curr_op, postfix_expression, opened_containers)
            else:
                raise FormattingError(f"Error: Invalid expression, did not recognize symbol '{symbol}'", i)

        # empty the operator stack if at the end of the expression
        while not self._op_stack.is_empty():
            curr_op = self._op_stack.pop()

            # if there are still left-operators with higher priority
            while ((not self._left_operators.is_empty())
                   and self._left_operators.top().get_priority() >= curr_op.get_priority()):
                postfix_expression.append(self._left_operators.pop())

            # if a container is encountered here, it has not been closed in the middle of the expression
            if isinstance(curr_op, operator.ContainerOperator):
                raise FormattingError(f"Error: Unclosed container '{curr_op.get_symbol()}', "
                                      f"missing '{curr_op.get_end_symbol()}'")

            postfix_expression.append(curr_op)

        while not self._left_operators.is_empty():
            postfix_expression.append(self._left_operators.pop())

        return postfix_expression
