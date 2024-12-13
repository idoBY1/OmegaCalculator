from typing import Dict

import src.calculatorLogic.expression_formatter as expression_formatter
import src.calculatorLogic.solver as solver
import src.userInteraction.user_interaction_handler as user_interaction_handler
import src.calculatorLogic.operator as operator


class OmegaDefinedOperators(operator.BaseDefinedOperators):
    """
    Defines the operators for the calculator. All the operations that can be performed by the calculator
    are defined in the dictionary provided by an instance of this class.
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


class Calculator:
    def __init__(self):
        """
        Create a new Calculator object.
        """
        self.defined_operators = OmegaDefinedOperators()

        self.user_interaction_handler = user_interaction_handler.ConsoleInteractionHandler()
        self.formatter = expression_formatter.InfixToPostfixFormatter(self.defined_operators.get_operators_dict())
        self.solver = solver.PostfixSolver(self.defined_operators.get_operators_dict())

    def run(self):
        """
        Run the Calculator.
        """
        user_input = self.user_interaction_handler.get_input_expression("Enter an expression: \n")
        symbol_list = self.formatter.extract_symbols(user_input)
        print(symbol_list)

        formatted_expression = self.formatter.format_expression(symbol_list)
        print([str(item) for item in formatted_expression])

        if formatted_expression == [] and symbol_list != []:
            return

        is_error_free, result = self.solver.solve(formatted_expression)

        if is_error_free:
            print(f"The result of the expression is: {result}")