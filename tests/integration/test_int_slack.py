"""integration tests for the messages.slack module."""

import pytest

from messages.slack import SlackWebhook, SlackPost
from messages._exceptions import MessageSendError

from conftest import skip_if_on_travisCI


#############################################################################
# FIXTURES
##############################################################################

@pytest.fixture()
def get_slackwebhook():
    """Return a valid SlackWebhook instance."""
    return SlackWebhook(
        subject='[Messages] Integration Test',
        body='Conducting Integration Testing',
        attachments='https://imgs.xkcd.com/comics/python.png')


@pytest.fixture()
def get_slackpost():
    """Return a valid SlackPost instance."""
    return SlackPost(
        channel='#tester',
        subject='[Messages] Integration Test',
        body='Conducting Integration Testing',
        attachments='https://imgs.xkcd.com/comics/python.png')


##############################################################################
# TESTS: Slack*.send()
##############################################################################

@skip_if_on_travisCI
def test_slackWH_send_good(get_slackwebhook, capsys):
    """
    GIVEN a valid SlackWebhook instance
    WHEN send() is called
    THEN assert it sends the message
    """
    s = get_slackwebhook
    s.send()
    out, err = capsys.readouterr()
    assert "Message sent" in out


@skip_if_on_travisCI
def test_slackWH_send_badAuth(get_slackwebhook):
    """
    GIVEN a valid SlackWebhook instance
    WHEN send() is called
    THEN assert it sends the message
    """
    s = get_slackwebhook
    s.url = 'https://hooks.slack.com/services/badAuthCreds'
    with pytest.raises(MessageSendError):
        s.send()


@skip_if_on_travisCI
def test_slackP_send(get_slackpost, capsys):
    """
    GIVEN a valid SlackPost instance
    WHEN send() is called
    THEN assert it sends the message
    """
    s = get_slackpost
    s.send()
    out, err = capsys.readouterr()
    assert "Message sent" in out
