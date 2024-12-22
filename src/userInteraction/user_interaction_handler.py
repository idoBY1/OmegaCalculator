from abc import ABC, abstractmethod
from typing import Tuple

import src.userInteraction.input_handler as input_handler
import src.userInteraction.output_handler as output_handler


class IUserInteractionHandler(ABC):
    """
    Interface for handling input and output from and to the user
    """
    _input_handler: input_handler.IInputHandler
    _output_handler: output_handler.IOutputHandler

    @abstractmethod
    def get_input(self, input_msg: str = "") -> str:
        """
        Ask for a mathematical expression from the user.
        :param input_msg: A string message to instruct the user. Defaults to an empty string.
        :return: The string input from the user.
        """
        pass

    @abstractmethod
    def display(self, msg: str, end: str = "\n") -> None:
        """
        Display a message to the user.
        :param msg: The message to display.
        :param end: A string at the end of the message. Defaults to a new-line-character.
        """
        pass

    @abstractmethod
    def get_input_or_exit(self, exit_input: str, input_msg: str = "") -> Tuple[bool, str]:
        """
        Wait for input from the user. If the user enters the specified exit-input return ``False`` as the first
        item in the returning tuple. The first value of the tuple will be ``True`` if the second value of
        the tuple (the string) has the input from the user.
        :param exit_input: The input that will make the function return ``False`` in the tuple.
        :param input_msg: The message to ask the user for input. Defaults to an empty string.
        :return: A tuple containing a bool as its first value and a string as its second value.
        """
        pass


class ConsoleInteractionHandler(IUserInteractionHandler):
    """
    Class for receiving and outputting text to the console (command-line).
    """

    def __init__(self):
        self._input_handler = input_handler.ConsoleInputHandler()
        self._output_handler = output_handler.ConsoleOutputHandler()

    def get_input(self, input_msg: str = "") -> str:
        self._output_handler.output_str(input_msg)
        return self._input_handler.get_input_str()

    def display(self, msg: str, end: str = "\n") -> None:
        self._output_handler.output_str(msg + end)

    def get_input_or_exit(self, exit_input: str, input_msg: str = "") -> Tuple[bool, str]:
        self._output_handler.output_str(input_msg)

        try:
            user_input = self._input_handler.get_input_str()
        except KeyboardInterrupt:
            self._output_handler.output_str(
                f"Detected KeyboardInterrupt, exiting program.\n"
            )
            return False, ""
        except EOFError:
            self._output_handler.output_str(
                f"Detected EOF, exiting program.\n"
            )
            return False, ""

        if user_input == exit_input:
            return False, ""
        else:
            return True, user_input
