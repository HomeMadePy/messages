"""messages._utils tests."""

import builtins
import re

import pytest

import messages._utils
from messages._utils import credential_property
from messages._utils import validate_property
from messages._utils import validate_input
from messages._utils import check_valid
from messages._utils import validate_email
from messages._utils import validate_facebook
from messages._utils import validate_twilio
from messages._utils import validate_slackwebhook
from messages._utils import validate_slackpost
from messages._utils import validate_telegrambot
from messages._utils import validate_whatsapp
from messages._utils import timestamp
from messages._utils import validus
from messages._exceptions import InvalidMessageInputError


##############################################################################
# FIXTURES
##############################################################################

class DummyClass:
    """Test class used for testing."""
    cred_param = credential_property('cred_param')
    normal_param = validate_property('normal_param')
    def __init__(self, cred_param, normal_param):
        self.cred_param, self.normal_param = cred_param, normal_param


@pytest.fixture()
def get_test_class():
    """Return an instance of TestClass."""
    return DummyClass('s3cr3t', 'information')


def val_test_func(item):
    """Test func for check_valid."""
    if item == 'BAD':
        return False
    return True


##############################################################################
# TEST: credential_property & validate_property
##############################################################################

def test_properties_instantiation(get_test_class, mocker):
    """
    GIVEN a message class that utilized both *_property factory functions
    WHEN instantiation occurs
    THEN assert credential_property and validate_property successfully execute
    """
    val_mock = mocker.patch.object(messages._utils, 'validate_input')
    t = get_test_class
    assert t.cred_param == '***obfuscated***'
    assert '_cred_param' in t.__dict__
    assert t._cred_param == 's3cr3t'
    assert t.normal_param == 'information'
    t.normal_param = 'new information'
    t.normal_param = 'even newer information'
    assert val_mock.call_count == 2


def test_credential_property(mocker):
    """
    GIVEN an attribute to make as a property
    WHEN credential_property is called
    THEN assert a property is returned
    """
    val_mock = mocker.patch.object(messages._utils, 'validate_input')
    param = credential_property('param')
    assert isinstance(param, property)


def test_validate_property(mocker):
    """
    GIVEN an attribute to make as a property
    WHEN validate_property is called
    THEN assert a property is returned
    """
    val_mock = mocker.patch.object(messages._utils, 'validate_input')
    param = validate_property('param')
    assert isinstance(param, property)


##############################################################################
# TEST: validate_input
##############################################################################

def test_val_input_NotSupported():
    """
    GIVEN a message object is instantiated
    WHEN validate_input() is called on a message object that is
        not supported for input validation
    THEN assert nothing happens
    """
    result = validate_input('NotSupported', 'attr', 'some_value')
    assert result == 1


@pytest.mark.parametrize('msg_type, func, result', [
    ('Email', 'validate_email', 0),
    ('Facebook', 'validate_facebook', 0),
    ('Twilio', 'validate_twilio', 0),
    ('SlackPost', 'validate_slackpost', 0),
    ('SlackWebhook', 'validate_slackwebhook', 0),
    ('TelegramBot', 'validate_telegrambot', 0),
    ('WhatsApp', 'validate_whatsapp', 0),
])
def test_val_input_supported(msg_type, func, result, mocker):
    """
    GIVEN a message object is instantiated
    WHEN validate_input() is called on a message object
    THEN assert the proper validate_* func is called and 0 is the return value
    """
    val_mock = mocker.patch.object(messages._utils, func)
    r = validate_input(msg_type, 'attr', 'some_value')
    assert val_mock.call_count == 1
    assert r == result


##############################################################################
# TEST: validate_*
##############################################################################

@pytest.mark.parametrize('msg_type, func, attr', [
    ('Email', validate_email, 'address'),
    ('Facebook', validate_facebook, 'to'),
    ('Facebook', validate_facebook, 'local_attachment'),
    ('Facebook', validate_facebook, 'remote_attachment'),
    ('Twilio', validate_twilio, 'from_'),
    ('Twilio', validate_twilio, 'attachments'),
    ('SlackWebhook', validate_slackwebhook, 'url'),
    ('TelegramBot', validate_telegrambot, 'id_num' ),
    ('WhatsApp', validate_whatsapp, 'from_'),
    ('WhatsApp', validate_whatsapp, 'attachments')
])
def test_val_funcs(msg_type, func, attr, mocker):
    """
    GIVEN a message instance
    WHEN validate_* is called
    THEN assert check_valid is called the requisite number of times
    """
    check_mock = mocker.patch.object(messages._utils, 'check_valid')
    func(attr, 'some_value')
    assert check_mock.call_count == 1


def test_val_slackPost(mocker):
    """
    GIVEN a slackPost instance
    WHEN validate_slackpost is called with the correct input type
    THEN assert nothing bad happens
    **SlackPost is tested separately from the parametrized test_val_func()
    test because validate_slackpost is written differently and cannot be
    tested the same way.
    """
    check_mock = mocker.patch.object(messages._utils, 'check_valid')
    validate_slackpost('channel', 'some_value')
    validate_slackpost('attachments', 'some_value')


def test_val_slackPost_raises():
    """
    GIVEN a slackPost instance
    WHEN validate_slackpost is called with incorrect input type
    THEN assert InvalideMessageInputError is raised
    **SlackPost is tested separately from the parametrized test_val_func()
    test because validate_slackpost is written differently and cannot be
    tested the same way.
    """
    with pytest.raises(InvalidMessageInputError):
        validate_slackpost('channel', 1)


##############################################################################
# TEST: check_valid
##############################################################################

def test_check_valid(get_test_class):
    """
    GIVEN a valid message object
    WHEN check_valid is called on requisite attributes
    THEN assert normal behavior and no exceptions raised
    """
    t = get_test_class
    for key, value in t.__dict__.items():
        check_valid('TestClass', key, value, val_test_func, 'required type')


def test_check_valid_listAttributes(get_test_class):
    """
    GIVEN a valid message object
    WHEN check_valid is called on requisite attributes that are lists
    THEN assert normal behavior and no exceptions raised
    """
    t = get_test_class
    t.listAttr = ['val1', 'val2']
    for key, value in t.__dict__.items():
        check_valid('TestClass', key, value, val_test_func, 'required type')


def test_check_valid_singleton_raisesExc(get_test_class):
    """
    GIVEN a message object with a single invalid input
    WHEN check_valid is called
    THEN assert InvalidMessageInputError is raised
    """
    t = get_test_class
    t.normal_param = 'BAD'
    with pytest.raises(InvalidMessageInputError):
        for key, value in t.__dict__.items():
            check_valid('TestClass', key, value, val_test_func, 'required type')


def test_check_valid_list_raisesExc(get_test_class):
    """
    GIVEN a message object with a list of invalid inputs
    WHEN check_valid is called
    THEN assert InvalidMessageInputError is raised
    """
    t = get_test_class
    t.normal_param = ['GOOD', 'BAD']
    with pytest.raises(InvalidMessageInputError):
        for key, value in t.__dict__.items():
            check_valid('TestClass', key, value, val_test_func, 'required_type')


##############################################################################
# TEST: timestamp
##############################################################################

def test_timestamp():
    """
    GIVEN a need for a timestamp (i.e. --verbose output)
    WHEN timestamp() is called
    THEN assert a timestamp as a string is returned
    """
    t = timestamp()
    #r = '^\d{4}-[A-Za-z]{3}-\d{1,2}\s{1}\d{2}:\d{2}:\d{2}$'
    #assert re.match(r, t)
    assert isinstance(t, str)
