"""messages._config tests."""

import pytest
import builtins

import jsonconfig

import messages._config
from messages._config import check_config_file
from messages._config import verify_profile_name
from messages._config import retrieve_data_from_config
from messages._config import retrieve_pwd_from_config
from messages._config import update_config_data
from messages._config import update_config_pwd
from messages._config import create_config_profile
from messages._config import display_required_items
from messages._config import get_user_ack
from messages._config import get_data_from_user
from messages._config import get_auth_from_user
from messages._config import configure_profile
from messages._config import write_data
from messages._config import write_auth
from messages._exceptions import UnknownProfileError


##############################################################################
# FIXTURES
##############################################################################

class Msg:
    """A test message class."""
    def __init__(self, from_=None, auth=None, profile=None, save=False):
        self.from_ = from_
        self.auth = auth
        self.profile = profile
        self.save = save
    def __iter__(self):
        return iter(self.__dict__)


class Cfg:
    """basic cfg class."""
    def __init__(self):
        self.data = {}
        self.pwd = {}
        self.filename = '/default/path'


@pytest.fixture()
def get_msg():
    return Msg(from_='me', auth='passw0rd', profile='myProfile')


@pytest.fixture()
def get_cfg():
    return Cfg()

##############################################################################
# TESTS: check_config_file
##############################################################################

def test_check_config_file_auth_given_save_false(cfg_mock, get_msg, mocker):
    """
    GIVEN a call to check_config_file()
    WHEN auth is given and save=False
    THEN assert correct funcs are called
    """
    vrfy_mock = mocker.patch.object(messages._config, 'verify_profile_name')
    rdata_mock = mocker.patch.object(messages._config, 'retrieve_data_from_config')
    rpwd_mock = mocker.patch.object(messages._config, 'retrieve_pwd_from_config')
    udata_mock = mocker.patch.object(messages._config, 'update_config_data')
    upwd_mock = mocker.patch.object(messages._config, 'update_config_pwd')
    msg = get_msg
    check_config_file(msg)
    assert vrfy_mock.call_count == 1
    assert rdata_mock.call_count == 1
    assert rpwd_mock.call_count == 0
    assert udata_mock.call_count == 0
    assert upwd_mock.call_count == 0


def test_check_config_file_auth_Notgiven_save_false(cfg_mock, get_msg, mocker):
    """
    GIVEN a call to check_config_file()
    WHEN auth is not given and save=False
    THEN assert correct funcs are called
    """
    vrfy_mock = mocker.patch.object(messages._config, 'verify_profile_name')
    rdata_mock = mocker.patch.object(messages._config, 'retrieve_data_from_config')
    rpwd_mock = mocker.patch.object(messages._config, 'retrieve_pwd_from_config')
    udata_mock = mocker.patch.object(messages._config, 'update_config_data')
    upwd_mock = mocker.patch.object(messages._config, 'update_config_pwd')
    msg = get_msg
    msg.auth = None
    check_config_file(msg)
    assert vrfy_mock.call_count == 1
    assert rdata_mock.call_count == 1
    assert rpwd_mock.call_count == 1
    assert udata_mock.call_count == 0
    assert upwd_mock.call_count == 0


def test_check_config_file_auth_given_save_true(cfg_mock, get_msg, mocker):
    """
    GIVEN a call to check_config_file()
    WHEN auth is given and save=True
    THEN assert correct funcs are called
    """
    vrfy_mock = mocker.patch.object(messages._config, 'verify_profile_name')
    rdata_mock = mocker.patch.object(messages._config, 'retrieve_data_from_config')
    rpwd_mock = mocker.patch.object(messages._config, 'retrieve_pwd_from_config')
    udata_mock = mocker.patch.object(messages._config, 'update_config_data')
    upwd_mock = mocker.patch.object(messages._config, 'update_config_pwd')
    msg = get_msg
    msg.save = True
    check_config_file(msg)
    assert vrfy_mock.call_count == 1
    assert rdata_mock.call_count == 1
    assert rpwd_mock.call_count == 0
    assert udata_mock.call_count == 1
    assert upwd_mock.call_count == 1


##############################################################################
# TESTS: verify_profile_name
##############################################################################

def test_verify_profile_name_normal(get_msg, get_cfg):
    """
    GIVEN a call to verify_profile_name
    WHEN profile name is in cfg.data
    THEN assert no exeception is raised
    """
    msg = get_msg
    cfg = get_cfg
    cfg.data['myProfile'] = {}
    verify_profile_name(msg, cfg)


def test_verify_profile_name_raises(get_msg, get_cfg):
    """
    GIVEN a call to verify_profile_name
    WHEN profile name is not in cfg.data
    THEN assert UnknownProfileError is raised
    """
    msg = get_msg
    cfg = get_cfg
    with pytest.raises(UnknownProfileError):
        verify_profile_name(msg, cfg)


##############################################################################
# TESTS: retrieve_data_from_config
##############################################################################

def test_ret_data_from_config(get_msg, get_cfg):
    """
    GIVEN a call to retrive_data_from_config
    WHEN msg has attrs that are None and the same attrs have
        values stored in cfg
    THEN msg attrs are updated with cfg values
    """
    msg = get_msg
    cfg = get_cfg
    # create some attributes to test
    msg.a, msg.b = None, None
    cfg.data = {'myProfile': {'a': 1, 'b': 2}}
    retrieve_data_from_config(msg, cfg)
    assert msg.a == 1
    assert msg.b == 2


##############################################################################
# TESTS: retrieve_pwd_from_config
##############################################################################

def test_ret_pwd_from_config_singular(get_msg, get_cfg):
    """
    GIVEN a call to retrieve_pwd_from_config
    WHEN the pwd is saved in cfg.pwd and is a string without
     '  :  ' joining multiple strings
    THEN assert it is returned as a string
    """
    msg = get_msg
    cfg = get_cfg
    cfg.pwd = {'myProfile_msg': 'n3w_passw0rd'}
    retrieve_pwd_from_config(msg, cfg)
    assert msg.auth == 'n3w_passw0rd'


def test_ret_pwd_from_config_parsed(get_msg, get_cfg):
    """
    GIVEN a call to retrieve_pwd_from_config
    WHEN the pwd is saved in cfg.pwd and is a string with
     '  :  ' joining multiple strings
    THEN assert it is returned as a tuple split by the '  :  '
        joiner
    """
    msg = get_msg
    cfg = get_cfg
    cfg.pwd = {'myProfile_msg': 'n3w :: passw0rd'}
    retrieve_pwd_from_config(msg, cfg)
    assert msg.auth == ('n3w', 'passw0rd')


##############################################################################
# TESTS: update_config_data
##############################################################################

def test_update_cfg_data(get_msg, get_cfg):
    """
    GIVEN a call to update_config_data()
    WHEN msg has updated values
    THEN assert they are overwritten in cfg
    """
    msg = get_msg
    cfg = get_cfg
    # create some differing values to check
    msg.a, msg.b = 1, 2
    cfg.data = {'myProfile': {'a': 5, 'b': 6}}
    update_config_data(msg, cfg)
    assert cfg.data['myProfile']['a'] == 1
    assert cfg.data['myProfile']['b'] == 2


##############################################################################
# TESTS: update_config_pwd
##############################################################################

def test_update_cfg_pwd_singular(get_msg, get_cfg):
    """
    GIVEN a call to update_cfg_pwd
    WHEN msg.auth is a single string
    THEN assert it stored in cfg as such
    """
    msg = get_msg
    cfg = get_cfg
    msg.auth = 'n3w_password'
    cfg.pwd = {'myProfile_msg': 'passw0rd'}
    update_config_pwd(msg, cfg)
    assert cfg.pwd['myProfile_msg'] == 'n3w_password'


def test_update_cfg_pwd_parsed(get_msg, get_cfg):
    """
    GIVEN a call to update_cfg_pwd
    WHEN msg.auth is a tuple
    THEN assert it stored in cfg as a string with ' :: ' as the
        joiner
    """
    msg = get_msg
    cfg = get_cfg
    msg.auth = ('n3w', 'super', 'password')
    cfg.pwd = {'myProfile_msg': 'passw0rd'}
    update_config_pwd(msg, cfg)
    assert cfg.pwd['myProfile_msg'] == 'n3w :: super :: password'

##############################################################################
# TESTS: create_config_profile
##############################################################################

def test_create_config_profile_noAck(mocker):
    """
    GIVEN a call to create_config_profile
    WHEN the user does not say 'y' or 'Y'
    THEN assert the correct sequence is called
    """
    display_mock = mocker.patch.object(messages._config, 'display_required_items')
    gack_mock = mocker.patch.object(messages._config, 'get_user_ack')
    gack_mock.return_value = False
    input_mock = mocker.patch.object(builtins, 'input')
    data_mock = mocker.patch.object(messages._config, 'get_data_from_user')
    auth_mock = mocker.patch.object(messages._config, 'get_auth_from_user')
    conf_mock = mocker.patch.object(messages._config, 'configure_profile')
    create_config_profile('msg')
    assert display_mock.call_count == 1
    assert gack_mock.call_count == 1
    assert input_mock.call_count == 0
    assert data_mock.call_count == 0
    assert auth_mock.call_count == 0
    assert conf_mock.call_count == 0


def test_create_config_profile_Ack(mocker):
    """
    GIVEN a call to create_config_profile
    WHEN the user does say 'y' or 'Y'
    THEN assert the correct sequence is called
    """
    display_mock = mocker.patch.object(messages._config, 'display_required_items')
    gack_mock = mocker.patch.object(messages._config, 'get_user_ack')
    gack_mock.return_value = True
    input_mock = mocker.patch.object(builtins, 'input')
    data_mock = mocker.patch.object(messages._config, 'get_data_from_user')
    auth_mock = mocker.patch.object(messages._config, 'get_auth_from_user')
    conf_mock = mocker.patch.object(messages._config, 'configure_profile')
    create_config_profile('msg')
    assert display_mock.call_count == 1
    assert gack_mock.call_count == 1
    assert input_mock.call_count == 1
    assert data_mock.call_count == 1
    assert auth_mock.call_count == 1
    assert conf_mock.call_count == 1


##############################################################################
# TESTS: display_required_items
##############################################################################

@pytest.mark.parametrize(['msg', 'expected'],[
    ('email', 'Email service password'),
    ('slackpost', 'Slack API authentication token'),
    ('slackwebhook', 'Slack API Webhook URL'),
    ('telegrambot', 'Telegram authorization token'),
    ('twilio', 'Twilio API account SID'),
])
def test_display_required_items(msg, expected, capsys):
    """
    GIVEN a call to display_required_items
    WHEN given a message type
    THEN assert the correct output prints
    """
    display_required_items(msg)
    out, err = capsys.readouterr()
    assert 'Configure a profile for:' in out
    assert 'You will need the following information:' in out
    assert 'Authorization/credentials required:' in out
    assert expected in out


##############################################################################
# TESTS: get_user_ack
##############################################################################

def test_get_user_ack_yes(mocker):
    """
    GIVEN a call to get_user_ack()
    WHEN the user gives 'y'
    THEN assert True is returned
    """
    input_mock = mocker.patch.object(builtins, 'input')
    input_mock.return_value = 'y'
    ack = get_user_ack()
    assert ack == True


def test_get_user_ack_no(mocker):
    """
    GIVEN a call to get_user_ack()
    WHEN the user gives 'n'
    THEN assert False is returned
    """
    input_mock = mocker.patch.object(builtins, 'input')
    input_mock.return_value = 'n'
    ack = get_user_ack()
    assert ack == False

##############################################################################
# TESTS: get_data_from_user
##############################################################################

@pytest.mark.parametrize(['msg', 'expected'], [
    ('email', 3),
    ('slackpost', 2),
    ('slackwebhook', 1),
    ('telegrambot', 1),
    ('twilio', 1),
])
def test_get_data_from_user(msg, expected, mocker):
    """
    GIVEN a call to get_data_from_user
    WHEN a specific message is specified
    THEN assert input is called the correct number of times
    """
    input_mock = mocker.patch.object(builtins, 'input')
    get_data_from_user(msg)
    assert input_mock.call_count == expected


##############################################################################
# TESTS: get_auth_from_user
##############################################################################

@pytest.mark.parametrize(['msg', 'expected'], [
    ('email', 1),
    ('slackpost', 1),
    ('slackwebhook', 1),
    ('telegrambot', 1),
    ('twilio', 2),
])
def test_get_auth_from_user(msg, expected, mocker):
    """
    GIVEN a call to get_auth_from_user
    WHEN a specific message is specified
    THEN assert getpass is called the correct number of times
    """
    getpass_mock = mocker.patch.object(messages._config, 'getpass')
    get_auth_from_user(msg)
    assert getpass_mock.call_count == expected


##############################################################################
# TESTS: configure_profile
##############################################################################


def test_configure_profile(cfg_mock, mocker, capsys):
    """
    GIVEN a call to configure_profile()
    WHEN given valid arguments
    THEN assert the correct funcs called and correct output prints
    """
    data_mock = mocker.patch.object(messages._config, 'write_data')
    auth_mock = mocker.patch.object(messages._config, 'write_auth')
    profile_name = 'newProfile'
    data = {'a': 1, 'b': 2}
    auth = {'auth': 'passw0rd'}
    configure_profile('msg', profile_name, data, auth)
    out, err = capsys.readouterr()
    assert data_mock.call_count == 1
    assert auth_mock.call_count == 1
    assert '[+] Configuration entry for <' in out
    assert profile_name in out
    assert '> created.' in out
    assert '[+] Configuration file location:' in out
    assert '/default/path' in out


##############################################################################
# TESTS: write_data
##############################################################################

def test_write_data(get_cfg):
    """
    GIVEN a call to write_data
    WHEN data params are given
    THEN assert the params are correctly stored
    """
    cfg = get_cfg
    profile_name = 'newProfile'
    data = {'a': 1, 'b': 2}
    msg_type = 'msg'
    write_data(msg_type, profile_name, data, cfg)
    assert cfg.data['newProfile']['msg'] == data


##############################################################################
# TESTS: write_auth
##############################################################################

@pytest.mark.parametrize(['msg', 'auth', 'pwd'], [
    ('email', {'auth': 's3cr3t'}, 's3cr3t'),
    ('slackpost', {'auth': 's3cr3t'}, 's3cr3t'),
    ('slackwebhook', {'auth': 's3cr3t'}, 's3cr3t'),
    ('telegrambot', {'auth': 's3cr3t'}, 's3cr3t'),
    ('twilio', {'auth_sid': 'ABCD', 'auth_token': '1234'}, 'ABCD :: 1234'),
])
def test_write_auth(msg, auth, pwd, get_cfg):
    """
    GIVEN a call to write_auth
    WHEN an auth param is given
    THEN assert it is correctly stored
    """
    cfg = get_cfg
    profile_name = 'newProfile'
    key_fmt = profile_name + '_' + msg
    write_auth(msg, profile_name, auth, cfg)
    assert cfg.pwd[key_fmt] == pwd
