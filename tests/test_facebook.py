"""messages.facebook tests."""

import pytest

import messages.facebook
from messages.facebook import Facebook
from messages.facebook import check_config_file
from messages._eventloop import MESSAGELOOP
from messages._exceptions import MessageSendError


##############################################################################
# FIXTURES
##############################################################################

@pytest.fixture()
def get_facebook(mocker):
    """Return a valid Facebook object."""
    configure_mock = mocker.patch.object(messages.facebook, 'check_config_file')
    return Facebook(from_='testAccount@mail.com',
                 to='12345',
                 auth='p@ssw0rd',
                 thread_type='user',
                 body='test text!',
                 local_attachment=['file1', 'file2'],
                 remote_attachment='https://imgs.xkcd.com/comics/python.png',
                 profile='tester',
                 save=False)


##############################################################################
# TESTS: Facebook.__init__
##############################################################################

def test_facebook_init(get_facebook):
    """
    GIVEN a need to create an Facebook object
    WHEN the user instantiates a new object with required args
    THEN assert Facebook object is created with given args
    """
    t = get_facebook
    assert t.from_ == 'testAccount@mail.com'
    assert t.to == '12345'
    assert t.thread_type == 'USER'
    assert t.auth == '***obfuscated***'
    assert '_auth' in t.__dict__
    assert t._auth == 'p@ssw0rd'
    assert t.body == 'test text!'
    assert t.local_attachment == ['file1', 'file2']
    assert t.remote_attachment == 'https://imgs.xkcd.com/comics/python.png'


##############################################################################
# TESTS: Facebook.__str__
##############################################################################

def test_facebook_str(get_facebook, capsys):
    """
    GIVEN a valid Facebook object
    WHEN the user calls print() on the Facebook object
    THEN assert the correct format prints
    """
    t = get_facebook
    expected = ('\nFrom: testAccount@mail.com'
                '\nTo: 12345'
                '\nThread Type: USER'
                '\nBody: \'test text!\''
                '\nLocal Attachments: [\'file1\', \'file2\']'
                '\nRemote Attachments: https://imgs.xkcd.com/comics/python.png'
                '\nMessage ID: None\n')
    print(t)
    out, err = capsys.readouterr()
    assert out == expected
    assert err == ''


##############################################################################
# TESTS: Facebook._add_body
##############################################################################

@pytest.mark.parametrize('local, remote, body, expected', [
    (None, None, None, "(Y)"),
    ('./file1', None, None, None),
    (None, 'http://url.com', None, None),
    (None, None, 'test msg', 'test msg')
])
def test_facebook_add_body(local, remote, body, expected, get_facebook):
    """
    GIVEN a valid Facebook object
    WHEN Facebook.send() is called
    THEN assert that Facebook objects with empty local and remote
    attachments as well as empty bodies automatically add "(Y)" to
    the body so the message sends.
    """
    t = get_facebook
    t.local_attachment = local
    t.remote_attachment = remote
    t.body = body

    t._add_body()
    assert t.body == expected



##############################################################################
# TESTS: Facebook.send
##############################################################################

def test_facebook_send_verbose_false(get_facebook, capsys, mocker):
    """
    GIVEN a valid Facebook object
    WHEN Facebook.send() is called
    THEN assert the correct functions are called, correct attributes
        updated and correct debug output is generated (using verbose flag
        set to False)
    """
    body_mock = mocker.patch.object(Facebook, '_add_body')
    client_mock = mocker.patch.object(messages.facebook, 'Client')

    t = get_facebook
    t.send()
    t.message_id = 12345
    out, err = capsys.readouterr()
    assert 'Debugging info' not in out
    assert 'Message created.' not in out
    assert 'Login successful' not in out
    assert 'Body sent' not in out
    assert 'Local attachment sent' not in out
    assert 'Remote attachment sent' not in out
    assert '* From: testAccount@mail.com' not in out
    assert '* To: 12345' not in out
    assert '* Body: \'test text!\'' not in out
    assert '* Local Attachments: [\'file1\', \'file2\']' not in out
    assert '* Remote Attachments: https://imgs.xkcd.com/comics/python.png' not in out
    assert '* Attachments: https://imgs.xkcd.com/comics/python.png' not in out
    assert '* Message ID: ' not in out
    assert 'Message sent.' in out
    assert err == ''


def test_facebook_send_verbose_true(get_facebook, capsys, mocker):
    """
    GIVEN a valid Facebook object
    WHEN Facebook.send() is called
    THEN assert the correct functions are called, correct attributes
        updated and correct debug output is generated (using verbose flag
        set to True)
    """
    body_mock = mocker.patch.object(Facebook, '_add_body')
    client_mock = mocker.patch.object(messages.facebook, 'Client')

    t = get_facebook
    t.verbose = True
    t.thread_type = 'GROUP'
    t.send()
    out, err = capsys.readouterr()
    assert 'Debugging info' in out
    assert 'Message created' in out
    assert 'Login successful' in out
    assert 'Body sent' in out
    assert 'Local attachment sent' in out
    assert 'Remote attachment sent' in out
    assert '* From: testAccount@mail.com' in out
    assert '* To: 12345' in out
    assert '* Thread Type: GROUP' in out
    assert '* Body: \'test text!\'' in out
    assert '* Local Attachments: [\'file1\', \'file2\']' in out
    assert '* Remote Attachments: https://imgs.xkcd.com/comics/python.png' in out
    assert '* Message ID: ' in out
    assert 'Message sent.' in out
    assert err == ''

def test_facebook_send_thread_id_raisesValueError(get_facebook, mocker):
    """
    GIVEN a valid Facebook object
    WHEN Facebook.send() causes an http error
    THEN assert MessageSendError is raised
    """
    body_mock = mocker.patch.object(Facebook, '_add_body')
    client_mock = mocker.patch.object(messages.facebook, 'Client')

    t = get_facebook
    t.thread_type = 'test'
    with pytest.raises(MessageSendError):
        t.send()


##############################################################################
# TESTS: Facebook.send_async
##############################################################################

def test_send_async(cfg_mock, get_facebook, mocker):
    """
    GIVEN a valid Facebook object
    WHEN Facebook.send_async() is called
    THEN assert it is added to the event loop for async sending
    """
    msg_loop_mock = mocker.patch.object(MESSAGELOOP, 'add_message')
    t = get_facebook
    t.send_async()
    assert msg_loop_mock.call_count == 1
