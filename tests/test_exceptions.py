"""messages.exceptions tests."""

import pytest

from messages.exceptions import InvalidMessageInputError
from messages.exceptions import UnsupportedMessageTypeError
from messages.exceptions import UnknownProfileError


##############################################################################
# TESTS: MessageInputError
##############################################################################

def test_InvalidMessageInputError(capsys):
    """
    GIVEN no object instantiated, just raise the exception
    WHEN the exception is raised with given args
    THEN assert it raises exception and prints proper output
    """
    with pytest.raises(InvalidMessageInputError):
        raise InvalidMessageInputError('Email', 'from_', 'email address')
        out, err = capsys.readouterr()
        expected = 'Invalid input for specified message class: Email'
        expected += '\n\t* argument: "from_"'
        expected += '\n\t* input type must be: email address\n'
        assert out == expected
        assert err == ''


def test_UnsupportedMessageTypeError_default(capsys):
    """
    GIVEN no object instantiated, just raise the exception
    WHEN the exception is raised with given args
    THEN assert it raises exception and prints proper output
    """
    with pytest.raises(UnsupportedMessageTypeError):
        raise UnsupportedMessageTypeError('BadType')
        out, err = capsys.readouterr()
        expected = 'Invalid input for specified message class: BadType\n'
        assert out == expected
        assert err == ''


def test_UnsupportedMessageTypeError_listarg(capsys):
    """
    GIVEN no object instantiated, just raise the exception
    WHEN the exception is raised with given args
    THEN assert it raises exception and prints proper output
    """
    with pytest.raises(UnsupportedMessageTypeError):
        raise UnsupportedMessageTypeError('BadType', {'m1', 'm2'})
        out, err = capsys.readouterr()
        expected = 'Invalid input for specified message class: BadType'
        expected += '\n\t* Supported message types: '
        expected += "{'m1', 'm2'}\n"
        assert out == expected
        assert err == ''


def test_UnknownProfileError(capsys):
    """
    GIVEN no object instantiated, just raise the exception
    WHEN the exception is raised with given args
    THEN assert it raises exception and prints proper output
    """
    with pytest.raises(UnknownProfileError):
        raise UnknownProfileError('unknown_user')
        out, err = capsys.readouterr()
        expected = 'Unknown Profile name: unknown_user\n'
        assert out == expected
        assert err == ''
