"""messages.config tests."""

import pytest
import builtins
from unittest.mock import patch

import jsonconfig

import messages.config
from messages.config import configure
from messages.config import set_default_profile
from messages.config import create_config
from messages.config import getpass
from messages.exceptions import UnknownProfileError


##############################################################################
# FIXTURES
##############################################################################

class Msg:
    """A test message class."""
    def __init__(self, from_, password, profile=None, save=False):
        self.config_kwargs = {'from_': from_, 'password': password,
                     'profile': profile, 'save': save}


@pytest.fixture()
def get_msg():
    return Msg(from_='me', password='passw0rd')


##############################################################################
# TESTS: configure
##############################################################################

def test_configure_profileNone_saveFalse(get_msg, cfg_mock):
    """
    GIVEN a valid message object
    WHEN `configure` is called with the specified args
    THEN assert appropriate attributes are set
    """
    msg = get_msg
    configure(msg, params=msg.config_kwargs, to_save={'from_'}, credentials={'password'})
    assert msg.from_ == 'me'
    assert msg.password == 'passw0rd'


def test_configure_profileYes_saveTrue(cfg_mock):
    """
    GIVEN a valid message object
    WHEN `configure` is called with the specified args
    THEN assert appropriate attributes are set
    """
    msg = Msg(from_='me', password='passw0rd', profile='myProf', save=True)
    configure(msg, params=msg.config_kwargs, to_save={'from_'}, credentials={'password'})
    assert msg.from_ == 'me'
    assert msg.password == 'passw0rd'


@patch.object(messages.config, 'getpass')
def test_configure_noPassword(getpass_mock, cfg_mock):
    """
    GIVEN a valid message object
    WHEN `configure` is called with the specified args
    THEN assert appropriate attributes are set
    """
    msg = Msg(from_='me', password=None, profile='NewProf', save=False)
    configure(msg, params=msg.config_kwargs, to_save={'from_'}, credentials={'password'})
    print(msg.password)
    assert getpass_mock.call_count == 1


##############################################################################
# TESTS: set_default_profile
##############################################################################

def test_set_default_profileGood(cfg_mock):
    """
    GIVEN a profile to make as the default
    WHEN set_default_profile(profile) is called
    THEN verify no errors occur with call to jsonconfig.Config
    """
    set_default_profile('tester')


def test_set_default_profileBad(cfg_mock):
    """
    GIVEN a profile to make as the default
    WHEN set_default_profile(profile) is called with an unknown profile name
    THEN assert UnknownProfileError is raised
    """
    with pytest.raises(UnknownProfileError):
        set_default_profile('UnknownProfile')


##############################################################################
# TESTS: create_config
##############################################################################

@patch.object(messages.config, 'getpass')
@patch.object(builtins, 'input')
def test_create_config_withParams(input_mock, getpass_mock, cfg_mock):
    create_config('email', 'myProfile', {'defaults': ['from_'],
        'credentials': ['password']})
