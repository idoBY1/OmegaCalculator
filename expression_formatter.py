from abc import ABC, abstractmethod

class IFormatter(ABC):
    @abstractmethod
    def format_str(self, expression: str) -> str:
        """
        Format the string expression to a readable form by a solver.
        :param expression: Expression as string (usually from user input)
        :return: A formated string expression
        """
        pass

    @abstractmethod
    def check_str_expression(self, expression: str) -> (bool, str):
        """
        Check if the formatter can format the string. Return ``True`` if it can,
        and ``False`` if it cannot. If the string cannot be formatted, returns a
        reason for failure.
        :param expression: Expression to be checked
        :return: A tuple with a bool indicating success and a string for description
        """
        pass

class InfixToPostfixFormatter(IFormatter):
    def format_str(self, expression: str) -> str:
        pass

    def check_str_expression(self, expression: str) -> (bool, str):
        pass