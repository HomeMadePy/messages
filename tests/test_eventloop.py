"""messages.eventloop tests."""

import pytest

import asyncio
from collections import deque
from unittest.mock import patch, Mock
from messages._eventloop import MessageLoop
from messages.exceptions import UnsupportedMessageTypeError


##############################################################################
# FIXTURES
##############################################################################

@pytest.fixture()
def get_messageloop():
    """Return a valid MessageLoop object."""
    return MessageLoop()


class MsgGood:
    """Good because there is a send() method."""
    def __init__(self): pass
    def send(self): pass


class MsgBad:
    """Bad because there is no send() method."""
    def __init__(self): pass


##############################################################################
# TESTS: MessageLoop.__init__
##############################################################################

def test_init(get_messageloop):
    """
    GIVEN a need to create an MessageLoop object
    WHEN the user instantiates a new object
    THEN assert MessageLoop object is created with given args
    """
    ml = get_messageloop
    assert ml is not None


##############################################################################
# TESTS: MessageLoop.add_message
##############################################################################

@patch.object(MessageLoop, 'send_loop')
def test_add_message_msgGood(send_loop_mock, get_messageloop):
    """
    GIVEN a valid MessageLoop object
    WHEN a valid message is added with the add_message method
    THEN assert it is added and send_loop() is called
    """
    ml = get_messageloop
    ml.add_message(MsgGood())
    assert send_loop_mock.call_count == 1


def test_add_message_msgBad(get_messageloop):
    """
    GIVEN a valid MessageLoop object
    WHEN an invalid message is added with the add_message method
    THEN assert UnsupportedMessageTypeError is raised
    """
    ml = get_messageloop
    with pytest.raises(UnsupportedMessageTypeError):
        ml.add_message(MsgBad())


##############################################################################
# TESTS: MessageLoop.send_loop
##############################################################################

def test_send_loop_MessageGood(get_messageloop):
    """
    GIVEN a valid MessageLoop object
    WHEN a send_loop() is initiated with a valid message
    THEN assert the loop.run_in_executor is called to send the message
    """
    ml = get_messageloop
    ml.loop = Mock()
    ml.add_message(MsgGood())
    assert ml.loop.run_in_executor.call_count == 1
