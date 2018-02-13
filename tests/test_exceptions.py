"""messages.exceptions tests."""

import pytest

from messages.exceptions import InvalidMessageInputError
from messages.exceptions import UnsupportedMessageTypeError


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


def test_UnsupportedMessageTypeError(capsys):
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
