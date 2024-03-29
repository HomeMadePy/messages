"""integration tests for messages.email_ module."""

import pathlib

import pytest

from messages.email_ import Email
from messages._exceptions import MessageSendError

from conftest import skip_if_on_travisCI


#############################################################################
# FIXTURES
##############################################################################

TESTDIR = pathlib.Path(__file__).absolute().parent.parent.joinpath('data')

@pytest.fixture()
def get_email():
    """Return a valid Email instance."""
    return Email(
        subject='[Messages] Integration Test',
        body='Conducting Integration Testing',
        attachments=str(TESTDIR.joinpath('file2.png')))


##############################################################################
# TESTS: Email.send()
##############################################################################

@skip_if_on_travisCI
def test_email_good(get_email, capsys):
    """
    GIVEN a good email instance
    WHEN sending the email
    THEN verify the send occurs without issue
    """
    e = get_email
    e.send()
    out, err = capsys.readouterr()
    assert "Message sent" in out


@skip_if_on_travisCI
def test_email_badAuth(get_email):
    """
    GIVEN a email with the wrong password
    WHEN sending the email
    THEN verify MessageSendError is raised
    """
    e = get_email
    e.auth = 'baDp@ssw0rd'

    with pytest.raises(MessageSendError):
        e.send()
