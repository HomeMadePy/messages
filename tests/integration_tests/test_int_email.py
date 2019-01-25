"""integration tests for messages.email_ module."""

import pathlib

import pytest
import int_setup

from messages.email_ import Email
from messages._exceptions import MessageSendError

##############################################################################
# SKIP TESTS IF ENVIRONMENT NOT PREPPED
##############################################################################

#Skip all tests if not configured
pytestmark = pytest.mark.skipif(not int_setup.integration_test_configured('email'),
    reason='Tester not configured for messages.email_.Email')


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
        profile='integration_tester',
        attachments=str(TESTDIR.joinpath('file2.png')),
        save=False)


##############################################################################
# TESTS: Email.send()
##############################################################################

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
