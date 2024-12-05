from abc import ABC, abstractmethod

import input_handler
import output_handler


class IUserInteractionHandler(ABC):
    _input_handler: input_handler.IInputHandler
    _output_handler: output_handler.IOutputHandler
    
    @abstractmethod
    def get_input_str(self) -> str:
        """
        Get input from the user as a string.
        :return: string of input from the user
        """
        pass

    @abstractmethod
    def output_str(self, output: str) -> None:
        """
        Output a string.
        :param output: The string to output
        """
        pass
