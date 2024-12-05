from abc import ABC, abstractmethod

class IOutputHandler(ABC):
    @abstractmethod
    def output_str(self, output: str) -> None:
        """
        Output a string.
        :param output: The string to output
        """
        pass

class ConsoleOutputHandler(IOutputHandler):
    def output_str(self, output: str) -> None:
        pass