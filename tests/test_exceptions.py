"""messages.exceptions tests."""

import pytest

from messages.exceptions import MessageInputError


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
        expected += '\n\targument: "from_"'
        expected += 'input type must be: email address\n'
        assert out == expected
        assert err == ''
