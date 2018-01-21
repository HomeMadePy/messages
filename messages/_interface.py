"""Interfaces for message classes."""


from abc import ABCMeta
from abc import abstractmethod


class Message(metaclass=ABCMeta):
    """Interface for standard message classes."""

    @abstractmethod
    def send(self):
        pass


    @abstractmethod
    def send_async(self):
        pass
