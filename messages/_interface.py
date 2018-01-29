"""Interfaces for message classes."""


from abc import ABCMeta
from abc import abstractmethod

from .utils import VALIDATOR


class Message(metaclass=ABCMeta):
    """Interface for standard message classes."""

    @abstractmethod
    def send(self):
        """Send message synchronously."""


    @abstractmethod
    def send_async(self):
        """Send message asynchronously."""


    def __setattr__(self, attr, val):
        """Validate attribute inputs after assignment."""
        self.__dict__[attr] = val
        VALIDATOR.validate_input(self, attr)
