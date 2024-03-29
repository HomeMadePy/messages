"""messages.email_ tests."""

import asyncio
import pathlib
import smtplib
from smtplib import SMTPResponseException
from email.mime.multipart import MIMEMultipart

import pytest

import messages
from messages.email_ import Email
from messages._exceptions import MessageSendError

from conftest import AsyncMock
from conftest import skip_if_on_travisCI
from conftest import skip_if_not_on_travisCI


TESTDIR = pathlib.Path(__file__).absolute().parent.joinpath('data')

##############################################################################
# FIXTURES
##############################################################################

@pytest.fixture()
def get_email(mocker):
    """Return a valid Email object."""
    e = Email(from_='me@here.com', to='you@there.com',
              server='smtp.gmail.com', port=465, auth='password',
              cc='someone@there.com', bcc=['them@there.com'],
              subject='subject', body='message', attachments=['file1', 'file2'])
    e.from_ = 'me@here.com'
    e.server = 'smtp.gmail.com'
    e.port = 465
    e.auth = 'password'
    return e


##############################################################################
# TESTS: Email.__init__
##############################################################################

def test_email_init_normal(get_email):
    """
    GIVEN a need to create an Email object
    WHEN the user instantiates a new object with required args
    THEN assert Email object is created with given args
    """
    e = get_email
    assert e is not None
    assert e.server == 'smtp.gmail.com'
    assert e.port == 465
    assert e.auth == '***obfuscated***'
    assert e.from_ == 'me@here.com'
    assert e.to == 'you@there.com'
    assert e.cc == 'someone@there.com'
    assert e.bcc == ['them@there.com']
    assert e.subject == 'subject'
    assert e.body == 'message'
    assert e.attachments == ['file1', 'file2']
    assert e.message is None


##############################################################################
# TESTS: Email.__str__
##############################################################################

def test_email_str(get_email, capsys):
    """
    GIVEN a valid Email object
    WHEN the user calls print() on the Email object
    THEN assert the correct format prints
    """
    e = get_email
    expected = ('\nServer: smtp.gmail.com:465'
                '\nFrom: me@here.com'
                '\nTo: you@there.com'
                '\nCc: someone@there.com'
                '\nBcc: [\'them@there.com\']'
                '\nSubject: subject'
                '\nBody: \'message\''
                '\nAttachments: [\'file1\', \'file2\']\n')
    print(e)
    out, err = capsys.readouterr()
    assert out == expected
    assert err == ''


##############################################################################
# TESTS: Email.get_server
##############################################################################

def test_get_server_known(get_email):
    """
    GIVEN a valid Email object
    WHEN get_server() is called with an email address
    THEN assert a known smtp server is returned
    """
    e = get_email
    server = e.get_server('me@gmail.com')
    assert server == ('smtp.gmail.com', 465)


def test_get_server_guess(get_email):
    """
    GIVEN a valid Email object
    WHEN get_server() is called with an email address
    THEN assert an smtp server guess is returned
    """
    e = get_email
    server = e.get_server('me@test.com')
    assert server == ('smtp.test.com', 465)


def test_get_server_noAddress(get_email):
    """
    GIVEN a valid Email object
    WHEN get_server() is called without an email address
    THEN assert (None, None) is returned
    """
    e = get_email
    e.from_ = None
    server = e.get_server(e.from_)
    assert server == (None, None)


##############################################################################
# TESTS: Email.list_to_string
##############################################################################

def test_list_to_string(get_email):
    """
    GIVEN a valid Email object
    WHEN given a list of recipients
    THEN assert the list is returned as a single string
    """
    e = get_email
    output = e.list_to_string(['her@there.com', 'him@there.com'])
    assert output == 'her@there.com, him@there.com'


##############################################################################
# TESTS: Email._construct_message
##############################################################################

def test_construct_message(get_email, mocker):
    """
    GIVEN a valid Email object
    WHEN Email._construct_message() is called
    THEN assert the email structure is created
    """
    header_mock = mocker.patch.object(Email, '_add_header')
    body_mock = mocker.patch.object(Email, '_add_body')
    attach_mock = mocker.patch.object(Email, '_add_attachments')
    e = get_email
    e._construct_message()
    assert isinstance(e.message, MIMEMultipart)
    assert header_mock.call_count == 1
    assert body_mock.call_count == 1
    assert attach_mock.call_count == 1


##############################################################################
# TESTS: Email._add_header
##############################################################################

def test_add_header(get_email, mocker):
    """
    GIVEN a valid Email object, where Email._construct_message() has been called
    WHEN Email.add_header() is called
    THEN assert correct parameters are set
    """
    body_mock = mocker.patch.object(Email, '_add_body')
    attach_mock = mocker.patch.object(Email, '_add_attachments')
    e = get_email
    e._construct_message()
    assert e.message['From'] == 'me@here.com'
    assert e.message['Subject'] == 'subject'


##############################################################################
# TESTS: Email._add_body
##############################################################################

def test_add_body(get_email, mocker):
    """
    GIVEN a valid Email object, where Email._construct_message() has been called
    WHEN Email.add_body() is called
    THEN assert body_text is attached
    """
    attach_mock = mocker.patch.object(Email, '_add_attachments')
    header_mock = mocker.patch.object(Email, '_add_header')
    mime_attach_mock = mocker.patch.object(MIMEMultipart, 'attach')
    e = get_email
    e._construct_message()
    assert mime_attach_mock.call_count == 1


##############################################################################
# TESTS: Email._add_attachments
##############################################################################

@skip_if_on_travisCI
def test_add_attachments_list_local(get_email, mocker):
    """
    GIVEN a valid Email object, where Email._construct_message() has been called
        and Email.attachments is a list
    WHEN Email.add_attachments() is called
    THEN assert correct attachments are attached
    """
    header_mock = mocker.patch.object(Email, '_add_header')
    body_mock = mocker.patch.object(Email, '_add_body')
    mime_attach_mock = mocker.patch.object(MIMEMultipart, 'attach')
    e = get_email
    e.attachments = [str(TESTDIR.joinpath('file1.txt')), str(TESTDIR.joinpath('file2.png')),
                     str(TESTDIR.joinpath('file3.pdf')), str(TESTDIR.joinpath('file4.xlsx'))]
    e._construct_message()
    assert mime_attach_mock.call_count == 4


@skip_if_not_on_travisCI
def test_add_attachments_list_travis(get_email, mocker):
    """
    GIVEN a valid Email object, where Email._construct_message() has been called
         and Email.attachments is a list
    WHEN Email.add_attachments() is called
    THEN assert correct attachments are attached
    """
    header_mock = mocker.patch.object(Email, '_add_header')
    body_mock = mocker.patch.object(Email, '_add_body')
    mime_attach_mock = mocker.patch.object(MIMEMultipart, 'attach')
    e = get_email
    PATH = '/home/travis/build/HomeMadePy/messages/tests/data/'
    e.attachments = [PATH + 'file1.txt', PATH + 'file2.png',
                     PATH + 'file3.pdf', PATH + 'file4.xlsx']
    e._construct_message()
    assert mime_attach_mock.call_count == 4


@skip_if_on_travisCI
def test_add_attachments_str_local(get_email, mocker):
    """
    GIVEN a valid Email object, where Email._construct_message() has been called
        and Email.attachments is a str
    WHEN Email.add_attachments() is called
    THEN assert correct attachments are attached
    """
    header_mock = mocker.patch.object(Email, '_add_header')
    body_mock = mocker.patch.object(Email, '_add_body')
    mime_attach_mock = mocker.patch.object(MIMEMultipart, 'attach')
    e = get_email
    e.attachments = str(TESTDIR.joinpath('file1.txt'))
    e._construct_message()
    assert mime_attach_mock.call_count == 1


@skip_if_not_on_travisCI
def test_add_attachments_str_travis(get_email, mocker):
    """
    GIVEN a valid Email object, where Email._construct_message() has been called
         and Email.attachments is a str
    WHEN Email.add_attachments() is called
    THEN assert correct attachments are attached
    """
    header_mock = mocker.patch.object(Email, '_add_header')
    body_mock = mocker.patch.object(Email, '_add_body')
    mime_attach_mock = mocker.patch.object(MIMEMultipart, 'attach')
    e = get_email
    PATH = '/home/travis/build/HomeMadePy/messages/tests/data/'
    e.attachments = PATH + 'file1.txt'
    e._construct_message()
    assert mime_attach_mock.call_count == 1


##############################################################################
# TESTS: Email._get_session
##############################################################################

def test_get_session_ssl(get_email, mocker):
    """
    GIVEN a valid Email object
    WHEN Email.get_session() is called
    THEN assert the correct functions are called
    """
    getssl_mock = mocker.patch.object(Email, '_get_ssl')
    e = get_email
    e._get_session()
    assert getssl_mock.call_count == 1


def test_get_session_tls(get_email, mocker):
    """
    GIVEN a valid Email object
    WHEN Email.get_session() is called
    THEN assert the correct functions are called
    """
    gettls_mock = mocker.patch.object(Email, '_get_tls')
    e = get_email
    e.port = 587
    e._get_session()
    assert gettls_mock.call_count == 1


def test_get_session_ssl_raisesMessSendErr(get_email, mocker):
    """
    GIVEN an incorrect password in a valid Email object
    WHEN Email.get_session() is called
    THEN assert Exception is raised
    """
    get_ssl_mock = mocker.patch.object(Email, '_get_ssl')
    get_ssl_mock.return_value.login.side_effect = SMTPResponseException(code=0, msg=b'')
    e = get_email
    with pytest.raises(MessageSendError):
        e._get_session()


def test_get_session_tls_raisesMessSendErr(get_email, mocker):
    """
    GIVEN an incorrect password in a valid Email object
    WHEN Email.get_session() is called
    THEN assert Exception is raised
    """
    get_tls_mock = mocker.patch.object(Email, '_get_tls')
    get_tls_mock.return_value.login.side_effect = SMTPResponseException(code=0, msg=b'')
    e = get_email
    e.port = 587
    with pytest.raises(MessageSendError):
        e._get_session()


##############################################################################
# TESTS: Email._get_ssl
##############################################################################

def test_get_ssl(get_email, mocker):
    """
    GIVEN a valid Email object
    WHEN Email.get_ssl() is called
    THEN assert an SMTP_SSL instance is invoked
    """
    smtpssl_mock = mocker.patch.object(smtplib, 'SMTP_SSL')
    e = get_email
    e._get_ssl()
    assert smtpssl_mock.call_count == 1


def test_get_ssl_port_string(get_email, mocker):
    """
    GIVEN a valid Email object
    WHEN port type is set to string
    THEN assert the correct functions are called
    """
    getssl_mock = mocker.patch.object(Email, '_get_ssl')
    e = get_email
    e.port = '465'
    e._get_session()
    assert getssl_mock.call_count == 1


##############################################################################
# TESTS: Email._get_tls
##############################################################################

def test_get_tls(get_email, mocker):
    """
    GIVEN a valid Email object
    WHEN Email.get_tls() is called
    THEN assert an SMTP instance is invoked
    """
    smtp_mock = mocker.patch.object(smtplib, 'SMTP')
    e = get_email
    e._get_tls()
    assert smtp_mock.call_count == 1


def test_get_tls_port_string(get_email, mocker):
    """
    GIVEN a valid Email object
    WHEN port type is set to string
    THEN assert the correct functions are called
    """
    gettls_mock = mocker.patch.object(Email, '_get_tls')
    e = get_email
    e.port = '587'
    e._get_session()
    assert gettls_mock.call_count == 1


##############################################################################
# TESTS: Email.send
##############################################################################

def test_send(get_email, capsys, mocker):
    """
    GIVEN a valid Email object
    WHEN Email.send() is called
    THEN assert the correct functions are called and correct attributes
        updated
    """
    header_mock = mocker.patch.object(Email, '_add_header')
    body_mock = mocker.patch.object(Email, '_add_body')
    attach_mock = mocker.patch.object(Email, '_add_attachments')
    session_mock = mocker.patch.object(Email, '_get_session')
    e = get_email
    e.send()
    out, err = capsys.readouterr()
    assert out == 'Message sent.\n'
    assert err == ''


def test_send_verbose_true(get_email, capsys, mocker):
    """
    GIVEN a valid Email object
    WHEN Email.send() is called
    THEN assert the correct functions are called, correct attributes
        updated and correct debug output is generated (using verbose flag
        set to True)
    """
    header_mock = mocker.patch.object(Email, '_add_header')
    body_mock = mocker.patch.object(Email, '_add_body')
    attach_mock = mocker.patch.object(Email, '_add_attachments')
    session_mock = mocker.patch.object(Email, '_get_session')
    e = get_email
    e.verbose = True
    e.send()
    out, err = capsys.readouterr()
    assert 'Debugging info' in out
    assert 'Message created.' in out
    assert 'Login successful.' in out
    assert 'Logged out.' in out
    assert ' * Server: smtp.gmail.com:465' in out
    assert ' * From: me@here.com' in out
    assert ' * To: you@there.com' in out
    assert ' * Cc: someone@there.com' in out
    assert ' * Bcc: [\'them@there.com\']' in out
    assert ' * Subject: subject' in out
    assert ' * Body: \'message\'' in out
    assert ' * Attachments: [\'file1\', \'file2\']' in out
    assert 'Message sent.' in out
    assert err == ''


def test_send_verbose_false(get_email, capsys, mocker):
    """
    GIVEN a valid Email object
    WHEN Email.send() is called
    THEN assert the correct functions are called, correct attributes
        updated and correct debug output is generated (using verbose flag
        set to False)
    """
    header_mock = mocker.patch.object(Email, '_add_header')
    body_mock = mocker.patch.object(Email, '_add_body')
    attach_mock = mocker.patch.object(Email, '_add_attachments')
    session_mock = mocker.patch.object(Email, '_get_session')
    e = get_email
    e.verbose = False
    e.send()
    out, err = capsys.readouterr()

    assert out == 'Message sent.\n'
    assert 'Debugging info' not in out
    assert 'Message created.' not in out
    assert 'Login successful.' not in out
    assert 'Logged out.' not in out
    assert ' * Server: smtp.gmail.com:465' not in out
    assert ' * From: me@here.com' not in out
    assert err == ''


##############################################################################
# TESTS: Email.send_async
##############################################################################

@pytest.mark.asyncio
async def test_send_async_ssl(get_email, mocker):
    """
    GIVEN a valid Email object with port=465
    WHEN Email.send_async() is called
    THEN assert calls aiosmtplib.send with ssl

    AsyncMock found in conftest.py
    """
    async_mock = mocker.patch("aiosmtplib.send", new_callable=AsyncMock)
    e = get_email
    e.attachments = None
    await e.send_async()
    async_mock.assert_called_with(
            message=e.message,
            hostname=e.server,
            port=e.port,
            username=e.from_,
            password=e._auth,
            use_tls=True,
        )


@pytest.mark.asyncio
async def test_send_async_tls(get_email, mocker):
    """
    GIVEN a valid Email object with port=587
    WHEN Email.send_async() is called
    THEN assert calls aiosmtplib.send with TLS

    AsyncMock found in conftest.py
    """
    async_mock = mocker.patch("aiosmtplib.send", new_callable=AsyncMock)
    e = get_email
    e.attachments = None
    e.port = 587
    await e.send_async()
    async_mock.assert_called_with(
            message=e.message,
            hostname=e.server,
            port=e.port,
            username=e.from_,
            password=e._auth,
            start_tls=True,
        )
