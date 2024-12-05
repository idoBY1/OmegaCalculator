from abc import ABC, abstractmethod

class IInputHandler(ABC):
    @abstractmethod
    def get_input_str(self) -> str:
        """
        Get input from the user as a string.
        :return: string of input from the user
        """
        pass


class ConsoleInputHandler(IInputHandler):
    def get_input_str(self) -> str:
        pass