"""messages.slack tests."""

import pytest
import requests

from messages.telegram import TelegramBot
from messages._eventloop import MESSAGELOOP


##############################################################################
# FIXTURES
##############################################################################

@pytest.fixture()
def get_tgram(cfg_mock):
    """Return a valid TelegramBot object."""
    return TelegramBot(bot_token='34563:ABCDEFG', chat_id='123456', body='message',
                attachments=['https://url1.com', 'https://url2.com'])


##############################################################################
# TESTS: TelegramBot.__init__
##############################################################################

def test_tgram_init(get_tgram):
    """
    GIVEN a need for a TelegramBot object
    WHEN instantiated
    THEN assert it is properly created
    """
    t = get_tgram
    assert t.body == 'message'
    assert isinstance(t.message, dict)


##############################################################################
# TESTS: TelegramBot.get_chat_id
##############################################################################

def test_tgram_getChatID(get_tgram, mocker):
    """
    GIVEN a TelegramBot instance with unknown chat_id of recipient
    WHEN get_chat_id() is called
    THEN assert proper data is returned
    """
    req_mock = mocker.patch.object(requests, 'get')
    req_mock.return_value.json.return_value = {'result': [{'message':{
        'from':{'username': 'YOU', 'id': '123456'}}}]}
    t = get_tgram
    id = t.get_chat_id('@YOU')
    assert id == '123456'


##############################################################################
# TESTS: TelegramBot.construct_message
##############################################################################

def test_tgram_construct_message(get_tgram):
    """
    GIVEN a valid TelegramBot object
    WHEN construct_message() is called
    THEN assert the message is properly created
    """
    t = get_tgram
    t.construct_message()
    assert t.message['text'] == 'message'


def test_tgram_construct_message_withFromSub(get_tgram):
    """
    GIVEN a valid TelegramBot object
    WHEN construct_message() is called
    THEN assert the message is properly created
    """
    t = get_tgram
    t.from_ = 'me'
    t.subject = 'this is a test'
    t.construct_message()
    expected = 'From: me\n' + 'Subject: this is a test\n' + 'message'
    assert t.message['text'] == expected


##############################################################################
# TESTS: TelegramBot.send_content
##############################################################################

def test_tgram_send_content(get_tgram, capsys, mocker):
    """
    GIVEN a valid TelegramBot object
    WHEN send_content() is called
    THEN assert the proper send sequence occurs
    """
    req_mock = mocker.patch.object(requests, 'post')
    req_mock.return_value.status_code = 200
    t = get_tgram
    t.send_content()
    out, err = capsys.readouterr()
    assert req_mock.call_count == 1
    assert out == 'Message sent...\n'
    assert err == ''


def test_tgram_send_content_statusGT300(get_tgram, capsys, mocker):
    """
    GIVEN a valid TelegramBot object
    WHEN send_content() is called but an error occurs, status_code > 300
    THEN assert the proper send sequence occurs
    """
    req_mock = mocker.patch.object(requests, 'post')
    req_mock.return_value.status_code = 403
    req_mock.return_value.text = 'test error'
    t = get_tgram
    t.send_content()
    out, err = capsys.readouterr()
    assert req_mock.call_count == 1
    assert out == 'Error while sending...\n' + 'test error\n'
    assert err == ''

##############################################################################
# TESTS: TelegramBot.send
##############################################################################

def test_send(get_tgram, mocker):
    con_mock = mocker.patch.object(TelegramBot, 'construct_message')
    send_cont_mock = mocker.patch.object(TelegramBot, 'send_content')
    t = get_tgram
    t.send()
    assert con_mock.call_count == 1
    assert send_cont_mock.call_count == 3


##############################################################################
# TESTS: TelegramBot.send_async
##############################################################################

def test_tgram_send_async(get_tgram, mocker):
    """
    GIVEN a valid TelegramBot object
    WHEN send_async() is called
    THEN assert the proper send sequence occurs
    """
    msgloop_mock = mocker.patch.object(MESSAGELOOP, 'add_message')
    t = get_tgram
    t.send_async()
    assert msgloop_mock.call_count == 1
