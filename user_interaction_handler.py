from abc import ABC, abstractmethod

import input_handler
import output_handler


class IUserInteractionHandler(ABC):
    _input_handler: input_handler.IInputHandler
    _output_handler: output_handler.IOutputHandler

    @abstractmethod
    def get_input_expression(self, input_msg: str) -> str:
        """
        Ask for a mathematical expression from the user.
        :param input_msg: A string message to instruct the user
        :return: The string input from the user
        """
        pass


class ConsoleInteractionHandler(IUserInteractionHandler):
    def __init__(self):
        self._input_handler = input_handler.ConsoleInputHandler()
        self._output_handler = output_handler.ConsoleOutputHandler()

    def get_input_expression(self, input_msg: str) -> str:
        self._output_handler.output_str(input_msg + " ")
        return self._input_handler.get_input_str()