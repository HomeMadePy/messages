"""messages.cli tests."""

import sys
from unittest.mock import patch

import pytest

import click
from click.testing import CliRunner

import messages.cli
from messages.cli import main
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
