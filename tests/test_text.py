"""messages.text tests."""

import pytest
import httpx

import messages.text
from messages.text import Twilio
from messages._exceptions import MessageSendError


##############################################################################
# FIXTURES
##############################################################################

@pytest.fixture()
def get_twilio():
    """Return a valid Twilio object."""
    t = Twilio(from_='+16198675309', to='+16195551212',
            auth=('test_sid', 'test_token'), body='test text!',
            attachments='https://imgs.xkcd.com/comics/python.png')
    t.from_ = '+16198675309'
    t.auth = ('test_sid', 'test_token')
    return t


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
    assert t.from_ == '+16198675309'
    assert t.to == '+16195551212'
    assert t.auth == '***obfuscated***'
    assert '_auth' in t.__dict__
    assert t._auth == ('test_sid', 'test_token')
    assert t.body == 'test text!'
    assert t.attachments == 'https://imgs.xkcd.com/comics/python.png'


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
    expected = ('\nFrom: +16198675309'
                '\nTo: +16195551212'
                '\nBody: \'test text!\''
                '\nAttachments: https://imgs.xkcd.com/comics/python.png'
                '\nSID: None\n')
    print(t)
    out, err = capsys.readouterr()
    assert out == expected
    assert err == ''


##############################################################################
# TESTS: Twilio.send
##############################################################################

def test_send_verbose_false_status201(get_twilio, capsys, mocker):
    """
    GIVEN a valid Twilio object
    WHEN Twilio.send() is called
    THEN assert the correct functions are called, correct attributes
        updated and correct debug output is generated (using verbose flag
        set to False)
    """
    msg_mock = mocker.patch.object(httpx, 'post')
    msg_mock.return_value.status_code = 201
    t = get_twilio
    t.send()
    t.sid = 12345
    out, err = capsys.readouterr()
    assert 'Debugging info' not in out
    assert 'Message created.' not in out
    assert '* From: +16198675309' not in out
    assert '* To: +16195551212' not in out
    assert '* Body: test text!' not in out
    assert '* Attachments: https://imgs.xkcd.com/comics/python.png' not in out
    assert '* SID: ' not in out
    assert '* HTTP status code:' not in out
    assert out == 'Message sent.\n'
    assert err == ''


def test_send_verbose_true_status201(get_twilio, capsys, mocker):
    """
    GIVEN a valid Twilio object
    WHEN Twilio.send() is called
    THEN assert the correct functions are called, correct attributes
        updated and correct debug output is generated (using verbose flag
        set to True)
    """
    msg_mock = mocker.patch.object(httpx, 'post')
    msg_mock.return_value.status_code = 201
    t = get_twilio
    t.verbose = True
    t.send()
    out, err = capsys.readouterr()
    assert 'Debugging info' in out
    assert 'Message created.' in out
    assert '* From: +16198675309' in out
    assert '* To: +16195551212' in out
    assert '* Body: \'test text!\'' in out
    assert '* Attachments: https://imgs.xkcd.com/comics/python.png' in out
    assert '* SID: ' in out
    assert '* HTTP status code: 201' in out
    assert 'Message sent.' in out
    assert err == ''


def test_send_status_raisesMessSendErr(get_twilio, mocker):
    """
    GIVEN a valid Twilio object
    WHEN Twilio.send() causes an http error
    THEN assert MessageSendError is raised
    """
    msg_mock = mocker.patch.object(httpx, 'post')
    msg_mock.return_value.raise_for_status.side_effect = httpx.RequestError("error")
    t = get_twilio
    with pytest.raises(MessageSendError):
        t.send()
