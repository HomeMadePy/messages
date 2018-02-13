"""messages._utils tests."""

import pytest
from unittest.mock import patch

from messages.exceptions import InvalidMessageInputError
from messages._utils import Validator
from messages._utils import validus


##############################################################################
# FIXTURES
##############################################################################

@pytest.fixture()
def get_validator():
    """Return a valid Validator object."""
    return Validator()


class Email:
    """Basic Email class used for testing."""
    def __init__(self, from_='me@here.com'):
        self.from_ = from_


@pytest.fixture()
def get_testemail():
    """Return a valid ForTest object for testing."""
    return Email()


##############################################################################
# TEST: Validator.validate_input
##############################################################################

@patch.object(Validator, '_is_valid')
def test_val_input_singular(isval_mock, get_validator, get_testemail):
    """
    GIVEN a valid Validator object
    WHEN validate_input() is called on a message object
        whose attribute is a singular valid input
    THEN assert _is_valid is called upon the correct attribute
    """
    v = get_validator
    e = get_testemail
    v.validate_input(e, 'from_')
    assert isval_mock.call_count == 1


@patch.object(Validator, '_is_valid')
def test_val_input_list(isval_mock, get_validator, get_testemail):
    """
    GIVEN a valid Validator object
    WHEN validate_input() is called on a message object
        whose attribute is a list of valid inputs
    THEN assert _is_valid is called upon all items in the attribute
    """
    v = get_validator
    e = get_testemail
    e.from_ = ['me@here.com', 'you@there.com']
    v.validate_input(e, 'from_')
    assert isval_mock.call_count == 2


@patch.object(Validator, '_is_valid')
def test_val_input_singular_raiseError(isval_mock, get_validator,
    get_testemail):
    """
    GIVEN a valid Validator object
    WHEN validate_input() is called on a message object
        whose attribute is a singular invalid input
    THEN assert InvalidMessageInputError is raised
    """
    v = get_validator
    e = get_testemail
    e.from_ = 'bademail'
    isval_mock.return_value = False
    with pytest.raises(InvalidMessageInputError):
        v.validate_input(e, 'from_')


@patch.object(Validator, '_is_valid')
def test_val_input_list_raiseError(isval_mock, get_validator,
    get_testemail):
    """
    GIVEN a valid Validator object
    WHEN validate_input() is called on a message object
        whose attribute is a list of invalid inputs
    THEN assert InvalidMessageInputError is raised
    """
    v = get_validator
    e = get_testemail
    e.from_ = ['bademail1', 'bademail2']
    isval_mock.return_value = False
    with pytest.raises(InvalidMessageInputError):
        v.validate_input(e, 'from_')


##############################################################################
# TEST: Validator._is_valid
##############################################################################

@patch.object(validus, 'isemail')
def test_isvalid_true(isemail_mock, get_validator, get_testemail):
    """
    GIVEN a valid Validator object
    WHEN when _is_valid() is called with upon a valid attribute
    THEN assert True is returned
    """
    v = get_validator
    e = get_testemail
    isemail_mock.return_value = True
    result = v._is_valid('EMAIL', 'from_', 'you@there.com')
    assert result == True


@patch.object(validus, 'isemail')
def test_isvalid_false(isemail_mock, get_validator, get_testemail):
    """
    GIVEN a valid Validator object
    WHEN when _is_valid() is called with upon an invalid attribute
    THEN assert False is returned
    """
    v = get_validator
    e = get_testemail
    isemail_mock.return_value = False
    result = v._is_valid('EMAIL', 'from_', 'bademail')
    assert result == False
