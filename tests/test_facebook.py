"""messages.facebook tests."""

import pytest

import messages.facebook
from messages.facebook import Facebook
from messages.facebook import check_config_file
from messages._eventloop import MESSAGELOOP


##############################################################################
# FIXTURES
##############################################################################

@pytest.fixture()
def get_facebook(mocker):
    """Return a valid Facebook object."""
    configure_mock = mocker.patch.object(messages.text, 'check_config_file')
    t = Facebook(from_='1xrickybobbyx1@gmail.com',
                 to='100030753302336',
                 auth='Welcome1!',
                 thread_type='user',
                 body='test text!',
                 local_attachment=['file1', 'file2'],
                 remote_attachment='https://imgs.xkcd.com/comics/python.png',
                 profile='tester', save=False)
    t.from_ = 'messagespytester@gmail.com'
    t.auth = 'Welcome1@'
    t.profile = 'tester'
    return t


##############################################################################
# TESTS: Facebook.__init__
##############################################################################

def test_facebook_init(get_facebook, cfg_mock):
    """
    GIVEN a need to create an Facebook object
    WHEN the user instantiates a new object with required args
    THEN assert Facebook object is created with given args
    """
    t = get_facebook
    assert t.from_ == 'messagespytester@gmail.com'
    assert t.to == '100030753302336'
    assert t.thread_type == 'USER'
    assert t.auth == '***obfuscated***'
    assert '_auth' in t.__dict__
    assert t._auth == 'Welcome1@'
    assert t.body == 'test text!'
    assert t.local_attachment == ['file1', 'file2']
    assert t.remote_attachment == 'https://imgs.xkcd.com/comics/python.png'


##############################################################################
# TESTS: Facebook.__str__
##############################################################################

def test_facebook_str(get_facebook,cfg_mock, capsys):
    """
    GIVEN a valid Facebook object
    WHEN the user calls print() on the Facebook object
    THEN assert the correct format prints
    """
    t = get_facebook
    expected = ('\nFrom: messagespytester@gmail.com'
                '\nTo: 100030753302336'
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
# TESTS: Facebook.send
##############################################################################

def test_send_verbose_false(get_facebook, cfg_mock, capsys):
    """
    GIVEN a valid Facebook object
    WHEN Facebook.send() is called
    THEN assert the correct functions are called, correct attributes
        updated and correct debug output is generated (using verbose flag
        set to False)
    """
    t = get_facebook
    t.send()
    t.message_id = 12345
    out, err = capsys.readouterr()
    assert 'Debugging info' not in out
    assert 'Message created.' not in out
    assert '* From: messagespytester@gmail.com' not in out
    assert '* To: 100030753302336' not in out
    assert '* Body: test text!' not in out
    assert '* Local Attachments: [\'file1\', \'file2\']' not in out
    assert '* Remote Attachments: https://imgs.xkcd.com/comics/python.png' not in out
    assert '* Attachments: https://imgs.xkcd.com/comics/python.png' not in out
    assert '* Message ID: ' not in out
    assert out == 'Message sent.\n'
    assert err == ''


def test_send_verbose_true(get_facebook, cfg_mock, capsys):
    """
    GIVEN a valid Facebook object
    WHEN Facebook.send() is called
    THEN assert the correct functions are called, correct attributes
        updated and correct debug output is generated (using verbose flag
        set to True)
    """
    t = get_facebook
    t.verbose = True
    t.send()
    out, err = capsys.readouterr()
    assert 'Debugging info' in out
    assert 'Message created.' in out
    assert '* From: messagespytester@gmail.com' in out
    assert '* To: 100030753302336' in out
    assert '* Body: \'test text!\'' in out
    assert '* Local Attachments: [\'file1\', \'file2\']' in out
    assert '* Remote Attachments: https://imgs.xkcd.com/comics/python.png' in out
    assert '* Message ID: ' in out
    assert 'Message sent.' in out
    assert err == ''


def test_send_thread_id_raisesValueError(get_facebook, cfg_mock):
    """
    GIVEN a valid Facebook object
    WHEN Facebook.send() causes an http error
    THEN assert ValueError is raised
    """
    t = get_facebook
    t.thread_type = 'test'
    with pytest.raises(ValueError):
        t.send()


def test_empty_message(get_facebook, cfg_mock):
    """
    GIVEN a valid Facebook object
    WHEN Facebook.send() is called
    THEN assert that Facebook objects with empty local and remote
    attachments as well as empty bodies automatically add "(Y)" to
    the body so the message sends.
    """
    t = get_facebook
    t.body = ''
    t.local_attachment = ''
    t.remote_attachment = ''
    t.send()
    assert t.body == '(Y)'
    assert t.local_attachment == ''
    assert t.remote_attachment == ''


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
