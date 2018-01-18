"""messages.text tests."""

import pytest

from collections import deque
from unittest.mock import patch

from messages.text import Twilio
from twilio.rest import Client


##############################################################################
# FIXTURES
##############################################################################

@pytest.fixture()
def get_twilio():
    """Return a valid Twilio object."""
    return Twilio('test_acct_sid', 'test_auth_token', '+16198675309',
                  '+16195551212', 'test text!',
                  'https://imgs.xkcd.com/comics/python.png')


##############################################################################
# TESTS: Twilio.__init__
##############################################################################

def test_twilio_init(get_twilio):
    """
    GIVEN a need to create an Twilio object
    WHEN the user instantiates a new object with required args
    THEN assert Twilio object is created with given args
    """
    t = get_twilio
    assert t is not None
    assert t.acct_sid == 'test_acct_sid'
    assert t.auth_token == 'test_auth_token'
    assert isinstance(t.client, Client)
    assert t.from_ == '+16198675309'
    assert t.to == '+16195551212'
    assert t.body == 'test text!'
    assert t.media_url == 'https://imgs.xkcd.com/comics/python.png'
    assert isinstance(t.sent_texts, deque)


##############################################################################
# TESTS: Twilio.__str__
##############################################################################

def test_twilio_str(get_twilio, capsys):
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
                '\n\tmedia_url: https://imgs.xkcd.com/comics/python.png\n')
    print(t)
    out, err = capsys.readouterr()
    assert out == expected
    assert err == ''


##############################################################################
# TESTS: Twilio.__repr__
##############################################################################

def test_twilio_str(get_twilio, capsys):
    """
    GIVEN a valid Twilio object
    WHEN the user calls repr(t) or `>>> t` on the Twilio object
    THEN assert the correct format prints
    """
    t = get_twilio
    expected = ('Twilio(test_acct_sid, test_auth_token, +16198675309, '
                '+16195551212, test text!, '
                'https://imgs.xkcd.com/comics/python.png)\n')
    print(repr(t))
    out, err = capsys.readouterr()
    assert out == expected
    assert err == ''


##############################################################################
# TESTS: Twilio.send
##############################################################################

@patch.object(Client, 'messages')
def test_send(messages_mock, get_twilio, capsys):
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
    assert len(t.sent_texts) == 1
