from typing import Dict, List

import src.calculatorLogic.expression_formatter as expression_formatter
import src.calculatorLogic.solver as solver
import src.userInteraction.user_interaction_handler as user_interaction_handler
import src.calculatorLogic.operator as operator
from src.calculatorLogic.calc_errors import FormattingError, CalculationError, SolvingError
from src.calculatorLogic.operator import Operator

EXIT_INPUT = "exit"

class OmegaDefinedOperators(operator.BaseDefinedOperators):
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

                if isinstance(prev_op, operator.ContainerOperator): # if start of an independent expression
                    return self._get_overloaded_by_class(op_symbol, operator.Minus)
                elif (isinstance(prev_op, operator.BinaryOperator) # if after an operator that requires a value
                      or (isinstance(prev_op, operator.UnaryOperator)
                          and prev_op.get_operand_pos() == operator.UnaryOperator.OperandPos.AFTER)):
                    return self._get_overloaded_by_class(op_symbol, operator.NegativeSign)
                else: # default case
                    return self._get_overloaded_by_class(op_symbol, operator.Subtraction)
            case _:
                return self._op_dict[op_symbol]


class Calculator:
    def __init__(self):
        """
        Create a new Calculator object.
        """
        self.defined_operators = OmegaDefinedOperators()

        self.user_interaction_handler = user_interaction_handler.ConsoleInteractionHandler()
        self.formatter = expression_formatter.InfixToPostfixFormatter(self.defined_operators)
        self.solver = solver.PostfixSolver()

    def run(self):
        """
        Run the Calculator.
        """
        self.user_interaction_handler.display(f"Enter expressions to evaluate "
                                              f"(enter '{EXIT_INPUT}' to exit the program): ")

        continue_running, user_input = self.user_interaction_handler.get_input_or_exit(EXIT_INPUT, ">>> ")

        while continue_running:
            symbol_list = self.formatter.extract_symbols(user_input)
            # print(symbol_list)

            if len(symbol_list) > 0 and symbol_list[0] == "help":
                self.user_interaction_handler.display("Type a mathematical expression to get a solution. "
                                                      "The possible operations are: ")

                self.user_interaction_handler.display(", ".join(self.defined_operators.get_symbols()), end="\n\n")
            else:
                try:
                    formatted_expression = self.formatter.format_expression(symbol_list)
                    # print([str(item) for item in formatted_expression])

                    result = self.solver.solve(formatted_expression)

                    self.user_interaction_handler.display(f"= {result}\n")
                except FormattingError as e:
                    self.user_interaction_handler.display(e.message)

                    if e.position >= 0:
                        position_msg_prefix = "At position: "
                        self.user_interaction_handler.display(position_msg_prefix, "")

                        self.user_interaction_handler.display("".join(symbol_list))

                        for i in range(min(e.position, len(symbol_list))):
                            self.user_interaction_handler.display(" " * len(symbol_list[i]), "")
                        self.user_interaction_handler.display(" " * len(position_msg_prefix), "")

                        if e.position < len(symbol_list):
                            self.user_interaction_handler.display("^" * len(symbol_list[e.position]))
                        else:
                            self.user_interaction_handler.display("^")
                    else:
                        self.user_interaction_handler.display("")
                except CalculationError as e:
                    self.user_interaction_handler.display(e.message, end="\n\n")
                except SolvingError as e:
                    self.user_interaction_handler.display(e.message, end="\n\n")
                except Exception as e:
                    self.user_interaction_handler.display(str(e), end="\n\n")

            # get next input from the user
            continue_running, user_input = self.user_interaction_handler.get_input_or_exit(EXIT_INPUT, ">>> ")

        self.user_interaction_handler.display("Exiting program...")
