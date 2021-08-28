"""messages._exceptions tests."""

import pytest

from messages._exceptions import InvalidMessageInputError
from messages._exceptions import UnsupportedMessageTypeError
from messages._exceptions import UnknownProfileError
from messages._exceptions import MessageSendError


def test_InvalidMessageInputError(capsys):
    """
    GIVEN no object instantiated, just raise the exception
    WHEN the exception is raised with given args
    THEN assert it raises exception and prints proper output
    """
    with pytest.raises(InvalidMessageInputError):
        raise InvalidMessageInputError('Email', 'from_', 'some_value', 'email address')


def test_UnsupportedMessageTypeError_default(capsys):
    """
    GIVEN no object instantiated, just raise the exception
    WHEN the exception is raised with given args
    THEN assert it raises exception and prints proper output
    """
    with pytest.raises(UnsupportedMessageTypeError):
        raise UnsupportedMessageTypeError('BadType')


def test_UnsupportedMessageTypeError_listarg(capsys):
    """
    GIVEN no object instantiated, just raise the exception
    WHEN the exception is raised with given args
    THEN assert it raises exception and prints proper output
    """
    with pytest.raises(UnsupportedMessageTypeError):
        raise UnsupportedMessageTypeError('BadType', {'m1', 'm2'})


def test_UnknownProfileError(capsys):
    """
    GIVEN no object instantiated, just raise the exception
    WHEN the exception is raised with given args
    THEN assert it raises exception and prints proper output
    """
    with pytest.raises(UnknownProfileError):
        raise UnknownProfileError('unknown_user')


def test_MessageSendError(capsys):
    """
    GIVEN no object instantiated, just raise the exception
    WHEN the exception is raised with given args
    THEN assert it raises exception and prints proper output
    """
    with pytest.raises(MessageSendError):
        raise MessageSendError('login failed')
