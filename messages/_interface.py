"""Interfaces for message classes."""

import reprlib
from abc import ABCMeta
from abc import abstractmethod

from ._utils import validate_input


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
        validate_input(self, attr)


    def __repr__(self):
        """repr(self) in debugging format with auth attr obfuscated."""
        class_name = type(self).__name__
        output = '{}('.format(class_name)
        for attr in self:
            if attr == 'auth':
                output += 'auth=***obfuscated***,\n'
            elif attr == 'body':
                output += '{}={!r},\n'.format(attr, reprlib.repr(getattr(self, attr)))
            else:
                output += '{}={!r},\n'.format(attr, getattr(self, attr))
        output += ')'
        return output


    def __iter__(self):
        return iter(self.__dict__)
