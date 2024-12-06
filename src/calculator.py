import src.calculatorLogic.expression_formatter as expression_formatter
import src.calculatorLogic.solver as solver
import src.userInteraction.input_handler as input_handler
import src.userInteraction.user_interaction_handler as user_interaction_handler


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
        s = self.user_interaction_handler.get_input_expression("Enter something: ")
        print(s)