"""messages.cli tests."""

import sys
from unittest.mock import patch

import pytest

import click
from click.testing import CliRunner

import messages.cli
from messages.cli import main
from messages.cli import _message_factory
from messages.exceptions import MessageTypeError
from messages.email_ import Email


##############################################################################
# FIXTURES
##############################################################################


##############################################################################
# TESTS: cli.main
##############################################################################

@patch.object(click, 'echo')
def test_no_args(echo_mock):
    """
    GIVEN a call to messages on the CLI
    WHEN no CLI args are given, i.e. `$ messages `
    THEN assert sys.exit is called after usage statements are printed
    """
    runner = CliRunner()
    runner.invoke(main, [], catch_exceptions=True)
    assert echo_mock.call_count == 2


@patch.object(click, 'echo')
def test_no_message_type(echo_mock):
    """
    GIVEN a call to messages on the CLI
    WHEN -t option is not used
    THEN assert sys.exit is called after usage statements are printed
    """
    runner = CliRunner()
    runner.invoke(main, ['-a', 'file'], catch_exceptions=True)
    assert echo_mock.call_count == 2


def test_unsupported_message_types():
    """
    GIVEN a call to messages on the CLI
    WHEN an unsupported message type is called
    THEN assert MessageTypeError is raised
    """
    runner = CliRunner()
    with pytest.raises(MessageTypeError):
        runner.invoke(main, ['-t', 'bad_type'], catch_exceptions=False)


##############################################################################
# TESTS: cli._message_factory
##############################################################################

def test_msg_factory_email():
    """
    GIVEN a call to _message_factory with the given CLI args
    WHEN 'type'==Email
    THEN assert an Email instance is created
    """
    args = {'type': 'EMAIL', 'from': 'me@here.com', 'recipient': ('you@there.com',),
    'carboncopy': (), 'blindcopy': (), 'subject': 'test message',
    'body': 'ABCDEFG', 'attach': ['file1', 'file2'], 'credentials': ['smtp.google.com', '465', 'password']}
    msg = _message_factory(**args)
    assert isinstance(msg, Email)


def test_msg_factory_twilio():
    pass


def test_msg_factory_slackwebhook():
    pass
