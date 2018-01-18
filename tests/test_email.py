"""messages.email tests."""

import pytest
import smtplib

from collections import deque
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from unittest.mock import patch

from messages.email import Email


##############################################################################
# FIXTURES
##############################################################################

@pytest.fixture()
def get_email():
    """Return a valid Email object."""
    return Email('smtp.gmail.com', 465, 'password', 'me@here.com',
                 'you@there.com', 'someone@there.com', 'them@there.com',
                 'subject', 'message', ['file1', 'file2'])


##############################################################################
# TESTS: Email.__init__
##############################################################################

def test_email_init(get_email):
    """
    GIVEN a need to create an Email object
    WHEN the user instantiates a new object with required args
    THEN assert Email object is created with given args
    """
    e = get_email
    assert e is not None
    assert e.server_name == 'smtp.gmail.com'
    assert e.server_port == 465
    assert e.password == 'password'
    assert e.from_ == 'me@here.com'
    assert e.to == 'you@there.com'
    assert e.cc == 'someone@there.com'
    assert e.bcc == 'them@there.com'
    assert e.subject == 'subject'
    assert e.body_text == 'message'
    assert e.attachments == ['file1', 'file2']
    assert e.email == 'Email not yet created'
    assert isinstance(e.sent_emails, deque)


##############################################################################
# TESTS: Email.__str__()
##############################################################################

def test_email_str(get_email, capsys):
    """
    GIVEN a valid Email object
    WHEN the user calls print() on the Email object
    THEN assert the correct format prints
    """
    e = get_email
    expected = ('MIMEMultipart Email:'
                '\n\tServer: smtp.gmail.com:465'
                '\n\tFrom: me@here.com'
                '\n\tTo: you@there.com'
                '\n\tCc: someone@there.com'
                '\n\tBcc: them@there.com'
                '\n\tSubject: subject'
                '\n\tbody_text: message...'
                '\n\tattachments: [\'file1\', \'file2\']\n')
    print(e)
    out, err = capsys.readouterr()
    assert out == expected
    assert err == ''


##############################################################################
# TESTS: Email.__repr__()
##############################################################################

def test_email_repr(get_email, capsys):
    """
    GIVEN a valid Email object
    WHEN the user calls repr(e) or `>>> e` on the Email object
    THEN assert the correct format prints
    """
    e = get_email
    expected = ("Email(smtp.gmail.com, 465, password, "
                "me@here.com, you@there.com, someone@there.com, "
                "them@there.com, subject, message, ['file1', 'file2'])\n")
    print(repr(e))
    out, err = capsys.readouterr()
    assert out == expected
    assert err == ''


##############################################################################
# TESTS: Email.list_to_string()
##############################################################################

def test_list_to_string(get_email):
    """
    GIVEN a valid Email object
    WHEN given a list of recipients
    THEN assert the list is returned as a single string
    """
    e = get_email
    e.to = e.list_to_string(['her@there.com', 'him@there.com'])
    assert e.to == 'her@there.com, him@there.com'


##############################################################################
# TESTS: Email.generate_email()
##############################################################################

@patch.object(Email, 'add_attachments')
@patch.object(Email, 'add_body')
@patch.object(Email, 'add_header')
def test_generate_email(header_mock, body_mock, attach_mock, get_email):
    """
    GIVEN a valid Email object
    WHEN Email.generate_email() is called
    THEN assert the email structure is created
    """
    e = get_email
    e.generate_email()
    assert isinstance(e.email, MIMEMultipart)
    assert header_mock.call_count == 1
    assert body_mock.call_count == 1
    assert attach_mock.call_count == 1


##############################################################################
# TESTS: Email.add_header()
##############################################################################

@patch.object(Email, 'add_attachments')
@patch.object(Email, 'add_body')
def test_add_header(body_mock, attach_mock, get_email):
    """
    GIVEN a valid Email object, where Email.generate_email() has been called
    WHEN Email.add_header() is called
    THEN assert correct parameters are set
    """
    e = get_email
    e.generate_email()
    assert e.email['From'] == 'me@here.com'
    assert e.email['Subject'] == 'subject'


##############################################################################
# TESTS: Email.add_body()
##############################################################################

@patch.object(MIMEMultipart, 'attach')
@patch.object(Email, 'add_attachments')
@patch.object(Email, 'add_header')
def test_add_body(header_mock, attach_mock, mime_attach_mock, get_email):
    """
    GIVEN a valid Email object, where Email.generate_email() has been called
    WHEN Email.add_body() is called
    THEN assert body_text is attached
    """
    e = get_email
    e.generate_email()
    assert mime_attach_mock.call_count == 1


##############################################################################
# TESTS: Email.add_attachments()
##############################################################################

@patch.object(MIMEMultipart, 'attach')
@patch.object(Email, 'add_header')
@patch.object(Email, 'add_body')
def test_add_attachments(body_mock, header_mock, mime_attach_mock, get_email):
    """
    GIVEN a valid Email object, where Email.generate_email() has been called
    WHEN Email.add_attachments() is called
    THEN assert correct attachments are attached
    """
    e = get_email
    e.attachments = ['./data/file1.txt', './data/file2.png',
                     './data/file3.pdf', './data/file4.xlsx']
    e.generate_email()
    assert mime_attach_mock.call_count == 4


##############################################################################
# TESTS: Email.get_session()
##############################################################################

@patch.object(smtplib, 'SMTP_SSL')
@patch.object(Email, 'generate_email')
def test_get_session(gen_email_mock, smtpssl_mock, get_email):
    """
    GIVEN a valid Email object
    WHEN Email.get_session() is called
    THEN assert the correct functions are called
    """
    e = get_email
    e.generate_email()
    session = e.get_session()
    assert smtpssl_mock.call_count == 1


##############################################################################
# TESTS: Email.send()
##############################################################################

@patch.object(Email, 'get_session')
@patch.object(Email, 'add_attachments')
@patch.object(Email, 'add_body')
@patch.object(Email, 'add_header')
def test_send(header_mock, body_mock, attach_mock, session_mock,
              get_email, capsys):
    """
    GIVEN a valid Email object
    WHEN Email.sent() is called
    THEN assert the correct functions are called and correct attributes
        updated
    """
    e = get_email
    e.send()
    out, err = capsys.readouterr()
    assert out == 'Message sent...\n'
    assert err == ''
    assert e.sent_emails[0] == repr(e)
