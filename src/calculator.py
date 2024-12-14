from typing import Dict, List

import src.calculatorLogic.expression_formatter as expression_formatter
import src.calculatorLogic.solver as solver
import src.userInteraction.user_interaction_handler as user_interaction_handler
import src.calculatorLogic.operator as operator
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
            print(symbol_list)

            formatted_expression = self.formatter.format_expression(symbol_list)
            print([str(item) for item in formatted_expression])

            # The format_expression function returns [] when an error occurred
            if not (formatted_expression == []):
                is_error_free, result = self.solver.solve(formatted_expression)

                if is_error_free:
                    print(f"= {result}")

            # get next input from the user
            continue_running, user_input = self.user_interaction_handler.get_input_or_exit(EXIT_INPUT, ">>> ")

        self.user_interaction_handler.display("Exiting program...")
