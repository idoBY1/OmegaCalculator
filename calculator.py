import expression_formatter
import input_handler
import solver
import user_interaction_handler


class Calculator:
    def __init__(self):
        """
        Create a new Calculator object.
        """
        self.user_interaction_handler = user_interaction_handler.ConsoleInteractionHandler()
        self.formatter = expression_formatter.InfixToPostfixFormatter()
        self.solver = solver.PostfixSolver()

    def run(self):
        """
        Run the Calculator.
        """
        pass