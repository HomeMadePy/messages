"""messages._utils tests."""

import pytest

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

def test_val_input_singular(get_validator, get_testemail, mocker):
    """
    GIVEN a valid Validator object
    WHEN validate_input() is called on a message object
        whose attribute is a singular valid input
    THEN assert _is_valid is called upon the correct attribute
    """
    isval_mock = mocker.patch.object(Validator, '_is_valid')
    v = get_validator
    e = get_testemail
    v.validate_input(e, 'from_')
    assert isval_mock.call_count == 1


def test_val_input_list(get_validator, get_testemail, mocker):
    """
    GIVEN a valid Validator object
    WHEN validate_input() is called on a message object
        whose attribute is a list of valid inputs
    THEN assert _is_valid is called upon all items in the attribute
    """
    isval_mock = mocker.patch.object(Validator, '_is_valid')
    v = get_validator
    e = get_testemail
    e.from_ = ['me@here.com', 'you@there.com']
    v.validate_input(e, 'from_')
    assert isval_mock.call_count == 2


def test_val_input_singular_raiseError(get_validator, get_testemail, mocker):
    """
    GIVEN a valid Validator object
    WHEN validate_input() is called on a message object
        whose attribute is a singular invalid input
    THEN assert InvalidMessageInputError is raised
    """
    isval_mock = mocker.patch.object(Validator, '_is_valid')
    v = get_validator
    e = get_testemail
    e.from_ = 'bademail'
    isval_mock.return_value = False
    with pytest.raises(InvalidMessageInputError):
        v.validate_input(e, 'from_')


def test_val_input_list_raiseError(get_validator, get_testemail, mocker):
    """
    GIVEN a valid Validator object
    WHEN validate_input() is called on a message object
        whose attribute is a list of invalid inputs
    THEN assert InvalidMessageInputError is raised
    """
    isval_mock = mocker.patch.object(Validator, '_is_valid')
    v = get_validator
    e = get_testemail
    e.from_ = ['bademail1', 'bademail2']
    isval_mock.return_value = False
    with pytest.raises(InvalidMessageInputError):
        v.validate_input(e, 'from_')


##############################################################################
# TEST: Validator._is_valid
##############################################################################

def test_isvalid_true(get_validator, get_testemail, mocker):
    """
    GIVEN a valid Validator object
    WHEN when _is_valid() is called with upon a valid attribute
    THEN assert True is returned
    """
    isemail_mock = mocker.patch.object(validus, 'isemail')
    v = get_validator
    e = get_testemail
    isemail_mock.return_value = True
    result = v._is_valid('EMAIL', 'from_', 'you@there.com')
    assert result == True


def test_isvalid_false(get_validator, get_testemail, mocker):
    """
    GIVEN a valid Validator object
    WHEN when _is_valid() is called with upon an invalid attribute
    THEN assert False is returned
    """
    isemail_mock = mocker.patch.object(validus, 'isemail')
    v = get_validator
    e = get_testemail
    isemail_mock.return_value = False
    result = v._is_valid('EMAIL', 'from_', 'bademail')
    assert result == False
