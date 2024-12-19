import src.calculatorLogic.expression_formatter as expression_formatter
import src.calculatorLogic.solver as solver
import src.userInteraction.user_interaction_handler as user_interaction_handler
from src.calculatorLogic import defined_operators, operator
from src.calculatorLogic.calc_errors import FormattingError, CalculationError, SolvingError

EXIT_INPUT = "quit"
HELP_INPUT = "help"

class Calculator:
    def __init__(self):
        """
        Create a new Calculator object.
        """
        self.defined_operators = defined_operators.OmegaDefinedOperators()

        self.user_interaction_handler = user_interaction_handler.ConsoleInteractionHandler()
        self.formatter = expression_formatter.InfixToPostfixFormatter(self.defined_operators)
        self.solver = solver.PostfixSolver()

    def calculate(self, expression: str) -> float:
        """
        Get a mathematical expression as a string solve it and return the answer.
        :param expression: Mathematical expression as a string.
        :return: The result of the expression.
        """
        symbol_list = self.formatter.extract_symbols(expression)

        formatted_expression = self.formatter.format_expression(symbol_list)

        return self.solver.solve(formatted_expression)

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

            if len(symbol_list) > 0 and symbol_list[0] == HELP_INPUT:
                self.user_interaction_handler.display("Type a mathematical expression to get a solution. "
                                                      "The possible operations are: ")

                self.user_interaction_handler.display(", ".join(
                    [s if not isinstance(op, operator.ContainerOperator) else s + op.get_end_symbol()
                     for (s, op) in self.defined_operators.get_operators_dict().items()]), end="\n\n")

                self.user_interaction_handler.display("Additional commands: \n"
                                                      f"{HELP_INPUT} - show this information.\n"
                                                      f"{EXIT_INPUT} - exit the program.\n")
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
