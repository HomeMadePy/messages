"""messages.eventloop tests."""

import pytest
import gevent

from collections import deque
from unittest.mock import patch
from messages._eventloop import MessageLoop


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
    assert isinstance(ml.messages, deque)


##############################################################################
# TESTS: MessageLoop.add_message
##############################################################################

@patch.object(MessageLoop, 'send_loop')
def test_add_message(send_loop_mock, get_messageloop):
    """
    GIVEN a valid MessageLoop object
    WHEN a message is added with the add_message method
    THEN assert it is added and send_loop() is called
    """
    ml = get_messageloop
    ml.add_message('message')
    assert len(ml.messages) == 1
    assert send_loop_mock.call_count == 1

##############################################################################
# TESTS: MessageLoop.send_loop
##############################################################################

@patch.object(gevent, 'spawn')
def test_send_loop_MessageGood(spawn_mock, get_messageloop):
    """
    GIVEN a valid MessageLoop object
    WHEN a send_loop() is initiated with a valid message
    THEN assert the message is spawned via gevent
    """
    ml = get_messageloop
    ml.messages.append(MsgGood())
    ml.send_loop()
    spawn_mock.call_count == 1


@patch.object(gevent, 'spawn')
def test_send_loop_MessageBad(spawn_mock, get_messageloop):
    """
    GIVEN a valid MessageLoop object
    WHEN a send_loop() is initiated without a valid message
    THEN assert the message is NOT spawned via gevent
    """
    ml = get_messageloop
    ml.messages.append(MsgBad())
    ml.send_loop()
    spawn_mock.call_count == 0
