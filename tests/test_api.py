"""messages.api tests."""

import uuid

import pytest

import messages.api
from messages.api import send
from messages.api import message_factory
from messages.api import err_exit
from messages.email_ import Email
from messages.facebook import Facebook
from messages.slack import SlackWebhook
from messages.slack import SlackPost
from messages.telegram import TelegramBot
from messages.text import Twilio
from messages.whatsapp import WhatsApp
from messages._exceptions import InvalidMessageInputError
from messages._exceptions import UnsupportedMessageTypeError
from messages._exceptions import UnknownProfileError
from messages._exceptions import MessageSendError


##############################################################################
# FIXTURES
##############################################################################

email_kwargs = {
    'server': 'smtp.gmail.com', 'port': 465,
    'auth': 'passw0rd', 'from_': 'me@here.com',
    'to': 'you@there.com', 'cc': None, 'bcc': None,
    'subject': 'TEST', 'body': 'this is a message',
    'attachments': None
}

facebook_kwargs = {
    'from_': 'testAccount@mail.com', 'auth': 'p@ssw0rd',
    'to': '12345', 'thread_type': 'USER', 'body': 'test msg',
    'local_attachment': None, 'remote_attachment': None,
}

slackwebhook_kwargs = {
    'auth': 'https://slack.com', 'body': 'Test message',
    'attachments': None, 'params': {'author_name': 'me'}
}

slackpost_kwargs = {
    'auth': '12345abcdef', 'channel': 'general',
    'body': 'Test message', 'attachments': None, 'params': {'author_name': 'me'}
}

telegrambot_kwargs = {
    'auth': '1234:ABCD', 'chat_id': '123456'
}

twilio_kwargs = {
    'auth': ('your sid', 'your token'),
    'from_': '+19998675309', 'to': '+19998675309', 'body': 'Test!',
    'attachments': 'https://www.google.com'
}


##############################################################################
# TESTS: send()
##############################################################################

def test_send_async_false(mocker):
    """
    GIVEN a need to create and send an email message
    WHEN api.send() is called
    THEN assert first the factory function returns a valid message instance
    """
    kwargs = email_kwargs
    fact_mock = mocker.patch.object(messages.api, 'message_factory')
    send('email', **kwargs)
    assert fact_mock.call_count == 1


def test_send_async_true(mocker):
    """
    GIVEN a need to create and send an email message
    WHEN api.send() is called
    THEN assert first the factory function returns a valid message instance
    """
    kwargs = email_kwargs
    fact_mock = mocker.patch.object(messages.api, 'message_factory')
    send('email', send_async=True, **kwargs)
    assert fact_mock.call_count == 1


def test_send_raisesMessSendErr(mocker):
    """
    GIVEN a call to api.send()
    WHEN a message encounters a send() error
    THEN assert SystemExit is raised
    """
    kwargs = email_kwargs
    fact_mock = mocker.patch.object(messages.api, 'message_factory')
    fact_mock.return_value.send.side_effect = MessageSendError('login fail')
    with pytest.raises(SystemExit):
        send('email', **kwargs)


##############################################################################
# TESTS: message_factory
##############################################################################

@pytest.mark.parametrize('msg_type, msg_class, msg_args', [
    ('email', Email, email_kwargs),
    ('facebook', Facebook, facebook_kwargs),
    ('twilio', Twilio, twilio_kwargs),
    ('slackwebhook', SlackWebhook, slackwebhook_kwargs),
    ('slackpost', SlackPost, slackpost_kwargs),
    ('telegrambot', TelegramBot, telegrambot_kwargs),
    ('whatsapp', WhatsApp, twilio_kwargs),
])
def test_message_factory_(msg_type, msg_class, msg_args, cfg_mock):
    """
    GIVEN a need to create a message with the specified kwargs
    WHEN message_factory is called
    THEN assert a valid instance instance is returned
    """
    kwargs = msg_args
    msg = message_factory(msg_type, **kwargs)
    assert isinstance(msg, msg_class)


def test_message_factory_keyerror(cfg_mock):
    """
    GIVEN a need to create a message object
    WHEN message_factory is called with an unsupported message type
    THEN assert UnsupportedMessageTypeError is raised
    """
    kwargs = email_kwargs
    with pytest.raises(UnsupportedMessageTypeError):
        msg = message_factory('bad', **kwargs)


def test_message_factory_raisesUnkProfErr(cfg_mock):
    """
    GIVEN a need to create a message object
    WHEN message_factory is called with an unknown profile name
    THEN assert message is printed and SystemExit is raised
    """
    kwargs = email_kwargs
    kwargs['profile'] = str(uuid.uuid4())
    with pytest.raises(SystemExit):
        msg = message_factory('email', **kwargs)


def test_message_factory_raisesInvalInpErr(cfg_mock):
    """
    GIVEN a need to create a message object
    WHEN message_factory is called with an invalid input type per the message
        class parameter requirements
    THEN assert message is printed and SystemExit is raised
    """
    kwargs = email_kwargs
    kwargs['to'] = 'not an email address'
    with pytest.raises(SystemExit):
        msg = message_factory('email', **kwargs)


##############################################################################
# TESTS: err_exit
##############################################################################

def test_err_exit(capsys):
    """
    GIVEN an exception raised in api functions
    WHEN err_exit is called
    THEN assert the message is printed and SystemExit is raised
    """
    with pytest.raises(SystemExit):
        err_exit('error: ', 'bad profile')
        out, err = capsys.readouterr()
        assert 'error:' in out
        assert 'bad profile' in out
