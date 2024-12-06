from abc import ABC, abstractmethod
from typing import Any


class IStack(ABC):
    @abstractmethod
    def push(self, item: Any) -> Any:
        """
        Push an item to the top of the stack.
        :param item: The item to push
        :return: The item pushed
        """
        pass

    @abstractmethod
    def top(self) -> Any:
        """
        Get the item at the top of the stack (without popping it).
        :return: The item at the top of the stack
        """
        pass

    @abstractmethod
    def pop(self) -> Any:
        """
        Pop the item at the top of the stack and return it.
        :return: The item popped
        """
        pass

    @abstractmethod
    def is_empty(self) -> bool:
        """
        Check if the stack is empty.
        :return: A boolean value, ``True`` if the stack is empty and ``False`` if the
        stack has at least one item
        """
        pass

    @abstractmethod
    def __len__(self) -> int:
        """
        Get the number of items in the stack
        :return: The number of items in the stack
        """
        pass

class ListStack(IStack):
    def __init__(self):
        self._items = []

    def push(self, item: Any) -> Any:
        self._items.append(item)

    def top(self) -> Any:
        return self._items[-1]

    def pop(self) -> Any:
        return self._items.pop()

    def is_empty(self) -> bool:
        return len(self._items) == 0

    def __len__(self) -> int:
        return len(self._items)