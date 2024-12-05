import expression_formatter
import input_handler
import solver

class Calculator:
    def __init__(self):
        """
        Create a new Calculator object.
        """
        self.input_handler = input_handler.ConsoleInputHandler()
        self.formatter = expression_formatter.InfixToPostfixFormatter()
        self.solver = solver.PostfixSolver()

    def run(self):
        """
        Run the Calculator.
        """
        pass