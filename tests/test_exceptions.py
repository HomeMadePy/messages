"""messages._exceptions tests."""

import pytest

from messages._exceptions import InvalidMessageInputError
from messages._exceptions import UnsupportedMessageTypeError
from messages._exceptions import UnknownProfileError


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
        raise InvalidMessageInputError('Email', 'from_', 'some_value', 'email address')
        out, err = capsys.readouterr()
        assert 'Invalid input for specified message class: Email' in out
        assert '* argument: "from_"' in out
        assert '* value given: some_value'
        assert '* input type must be: email address' in out
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
        assert 'Invalid input for specified message class: BadType' in out
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
        assert 'Invalid input for specified message class: BadType' in out
        assert '* Supported message types:' in out
        assert "{'m1', 'm2'}" in out
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
        assert 'Unknown Profile name: unknown_user' in out
        assert err == ''
