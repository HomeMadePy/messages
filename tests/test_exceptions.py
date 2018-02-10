"""messages.exceptions tests."""

import pytest

from messages import MESSAGES
from messages.exceptions import MessageInputError
from messages.exceptions import MessageTypeError


##############################################################################
# TESTS: MessageInputError
##############################################################################

def test_MessageInputError(capsys):
    """
    GIVEN no object instantiated, just raise the exception
    WHEN the exception is raised with given args
    THEN assert it raises exception and prints proper output
    """
    with pytest.raises(MessageInputError):
        raise MessageInputError('Email', 'from_', 'email address')
        out, err = capsys.readouterr()
        expected = 'Invalid input for specified message class: Email'
        expected += '\n\t* argument: "from_"'
        expected += '\n\t* input type must be: email address\n'
        assert out == expected
        assert err == ''


def test_MessageTypeError(capsys):
    """
    GIVEN no object instantiated, just raise the exception
    WHEN the exception is raised with given args
    THEN assert it raises exception and prints proper output
    """
    with pytest.raises(MessageTypeError):
        raise MessageTypeError('BadType')
        out, err = capsys.readouterr()
        expected = 'Invalid input for specified message class: BadType'
        expected += '\n\t* Supported Message Types: '
        expected += (str(MESSAGES) + '\n')
        assert out == expected
        assert err == ''
