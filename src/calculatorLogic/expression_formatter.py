from abc import ABC, abstractmethod


class IFormatter(ABC):
    @abstractmethod
    def format_str(self, expression: str) -> str:
        """
        Format the string expression to a readable form by a solver.
        :param expression: Expression as string (usually from user input)
        :return: A formatted string expression
        """
        pass


class InfixToPostfixFormatter(IFormatter):
    def format_str(self, expression: str) -> str:
        pass
