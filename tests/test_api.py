"""messages.api tests."""

import pytest
from unittest.mock import patch, Mock

import messages.api
from messages.api import send
from messages.api import message_factory
from messages.email_ import Email
from messages.exceptions import UnsupportedMessageTypeError
from messages.slack import SlackWebhook
from messages.text import Twilio


##############################################################################
# FIXTURES
##############################################################################

@pytest.fixture()
def email_kwargs():
    return {'server': 'smtp.gmail.com', 'port': 465,
            'password': 'passw0rd', 'from_': 'me@here.com',
            'to': 'you@there.com', 'cc': None, 'bcc': None,
            'subject': 'TEST', 'body': 'this is a message',
            'attachments': None}


@pytest.fixture()
def slackwebhook_kwargs():
    return {'url': 'https://slack.com', 'body': 'Test message',
            'attachments': None, 'params': {'author_name': 'me'}}


@pytest.fixture()
def twilio_kwargs():
    return {'acct_sid': 'your sid', 'auth_token': 'your token',
            'from_': '+19998675309', 'to': '+19998675309', 'body': 'Test!',
            'attachments': 'https://www.google.com'}


##############################################################################
# TESTS: send()
##############################################################################

@patch.object(messages.api, 'message_factory')
def test_send_async_false(fact_mock, email_kwargs):
    """
    GIVEN a need to create and send an email message
    WHEN api.send() is called
    THEN assert first the factory function returns a valid message instance
    """
    kwargs = email_kwargs
    send('email', **kwargs)
    assert fact_mock.call_count == 1


@patch.object(messages.api, 'message_factory')
def test_send_async_true(fact_mock, email_kwargs):
    """
    GIVEN a need to create and send an email message
    WHEN api.send() is called
    THEN assert first the factory function returns a valid message instance
    """
    kwargs = email_kwargs
    send('email', send_async=True, **kwargs)
    assert fact_mock.call_count == 1


##############################################################################
# TESTS: message_factory
##############################################################################

def test_message_factory_keyerror(email_kwargs, cfg_mock):
    """
    GIVEN a need to create a message object
    WHEN message_factory is called with an unsupported message type
    THEN assert UnsupportedMessageTypeError is raised
    """
    kwargs = email_kwargs
    with pytest.raises(UnsupportedMessageTypeError):
        msg = message_factory('bad', **kwargs)


def test_message_factory_email(email_kwargs, cfg_mock):
    """
    GIVEN a need to create an email message with the specified kwargs
    WHEN message_factory is called
    THEN assert an Email instance is returned
    """
    kwargs = email_kwargs
    msg = message_factory('email', **kwargs)
    assert isinstance(msg, Email)


def test_message_factory_slackwebhook(slackwebhook_kwargs, cfg_mock):
    """
    GIVEN a need to create a slackwebhook message with the specified kwargs
    WHEN message_factory is called
    THEN assert a SlackWebhook instance is returned
    """
    kwargs = slackwebhook_kwargs
    msg = message_factory('slackwebhook', **kwargs)
    assert isinstance(msg, SlackWebhook)


def test_message_factory_twilio(twilio_kwargs, cfg_mock):
    """
    GIVEN a need to create a twilio message with the specified kwargs
    WHEN message_factory is called
    THEN assert a Twilio instance is returned
    """
    kwargs = twilio_kwargs
    msg = message_factory('twilio', **kwargs)
    assert isinstance(msg, Twilio)
