import expression_formatter
import input_handler

class Calculator:
    def __init__(self):
        """
        Create a new Calculator object.
        """
        self.input_handler = input_handler.ConsoleInputHandler()
        self.formatter = expression_formatter.InfixToPostfixFormatter()

    def run(self):
        """
        Run the Calculator.
        """
        pass