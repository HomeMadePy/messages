"""messages.text tests."""

import pytest

from collections import deque
from unittest.mock import patch

from twilio.rest import Client

import messages.text
from messages.text import Twilio
from messages.text import configure
from messages._eventloop import MESSAGELOOP


##############################################################################
# FIXTURES
##############################################################################

@pytest.fixture()
@patch.object(messages.text, 'configure')
def get_twilio(config_mock):
    """Return a valid Twilio object."""
    t = Twilio(from_='+16198675309', to='+16195551212', acct_sid='test_sid',
        auth_token='test_token', body='test text!',
        attachments='https://imgs.xkcd.com/comics/python.png',
        profile='tester', save=False)
    t.from_ = '+16198675309'
    t.acct_sid = 'test_sid'
    t.auth_token = 'test_token'
    t.profile = 'tester'
    return t


##############################################################################
# TESTS: Twilio.__init__
##############################################################################

def test_twilio_init(get_twilio, cfg_mock):
    """
    GIVEN a need to create an Twilio object
    WHEN the user instantiates a new object with required args
    THEN assert Twilio object is created with given args
    """
    t = get_twilio
    assert t.from_ == '+16198675309'
    assert t.to == '+16195551212'
    assert t.acct_sid == 'test_sid'
    assert t.auth_token == 'test_token'
    assert t.body == 'test text!'
    assert t.attachments == 'https://imgs.xkcd.com/comics/python.png'
    assert t.client is None
    assert isinstance(t.sent_messages, deque)


##############################################################################
# TESTS: Twilio.__str__
##############################################################################

def test_twilio_str(get_twilio,cfg_mock, capsys):
    """
    GIVEN a valid Twilio object
    WHEN the user calls print() on the Twilio object
    THEN assert the correct format prints
    """
    t = get_twilio
    expected = ('Twilio Text Message:'
                '\n\tFrom: +16198675309'
                '\n\tTo: +16195551212'
                '\n\tbody: test text!...'
                '\n\tattachments: https://imgs.xkcd.com/comics/python.png\n')
    print(t)
    out, err = capsys.readouterr()
    assert out == expected
    assert err == ''


##############################################################################
# TESTS: Twilio.get_client
##############################################################################

@patch.object(messages.text, 'Client')
def test_get_client(get_twilio):
    """
    GIVEN a valid Twilio object
    WHEN Twilio.get_client is called
    THEN assert a twilio.rest.Client is returned (a Mock object)
    """
    t = get_twilio
    client = t.get_client()
    assert client is not None


##############################################################################
# TESTS: Twilio.send
##############################################################################

@patch.object(Client, 'messages')
def test_send(messages_mock, get_twilio, cfg_mock, capsys):
    """
    GIVEN a valid Twilio object
    WHEN Twilio.send() is called
    THEN assert the correct functions are called and correct attributes
        updated
    """
    t = get_twilio
    t.send()
    t.sid = 12345
    out, err = capsys.readouterr()
    assert out == 'Message sent...\n'
    assert err == ''
    assert len(t.sent_messages) == 1


##############################################################################
# TESTS: Twilio.send_async
##############################################################################

@patch.object(MESSAGELOOP, 'add_message')
def test_send_async(msg_loop_mock, cfg_mock, get_twilio):
    """
    GIVEN a valid Twilio object
    WHEN Twilio.send_async() is called
    THEN assert it is added to the event loop for async sending
    """
    t = get_twilio
    t.send_async()
    assert msg_loop_mock.call_count == 1
