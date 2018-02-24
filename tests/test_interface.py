"""messages._interface tests."""

import pytest
from unittest.mock import patch

import messages._interface
from messages._interface import Message


##############################################################################
# FIXTURES
##############################################################################

class MsgGood(Message):
    """Good Message class since it has all required abstract methods."""
    def __init__(self, x, y):
        self.x, self.y = x, y
    def send(self): pass
    def send_async(self): pass


class MsgBad1(Message):
    """Bad Message class since it is missing one required abstract methods."""
    def __init__(self): pass
    def send(self): pass


class MsgBad2(Message):
    """Bad Message class since it is missing one required abstract methods."""
    def __init__(self): pass
    def send_async(self): pass


##############################################################################
# TESTS: instantiation
##############################################################################

@patch.object(messages._interface, 'VALIDATOR')
def test_MsgGood(val_mock):
    """
    GIVEN a message class that inherits from 'Message'
    WHEN instantiated with all required abstract methods
    THEN assert it is created
    """
    msg = MsgGood(1, 2)
    assert msg is not None


def test_MsgBad1():
    """
    GIVEN a message class that inherits from 'Message'
    WHEN instantiated with missing required abstract methods
    THEN assert
    """
    with pytest.raises(TypeError):
        msg = MsgBad1()


def test_MsgBad2():
    """
    GIVEN a message class that inherits from 'Message'
    WHEN instantiated with missing required abstract methods
    THEN assert
    """
    with pytest.raises(TypeError):
        msg = MsgBad2()


##############################################################################
# TESTS: __setattr__
##############################################################################

@patch.object(messages._interface, 'VALIDATOR')
def test_setattr(val_mock):
    """
    GIVEN a message class that inherits from 'Message'
    WHEN instantiated with all required abstract methods
    THEN assert VALIDATOR.validate_input is called once per attribute (2)
    """
    msg = MsgGood(1, 2)
    assert val_mock.validate_input.call_count == 2


##############################################################################
# TESTS: __repr__
##############################################################################

@patch.object(messages._interface, 'VALIDATOR')
def test_repr(val_mock, capsys):
    """
    GIVEN a message class that inherits from 'Message'
    WHEN repr(msg) or `>>> msg` is called
    THEN assert appropriate output is printed
    """
    msg = MsgGood(1, 2)
    print(repr(msg))
    out, err = capsys.readouterr()
    expected = '<messages.MsgGood class> at: '
    assert expected in out
    assert err == ''


##############################################################################
# TESTS: __iter__
##############################################################################

@patch.object(messages._interface, 'VALIDATOR')
def test_iter(val_mock):
    """
    GIVEN a message class that inherits from 'Message'
    WHEN an iterator-type function is called (such as set(msg))
    THEN assert all defined attributes are returned
    """
    msg = MsgGood(1, 2)
    s = set(msg)
    assert s == {'x', 'y'}
