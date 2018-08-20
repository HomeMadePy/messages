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
    return TelegramBot(auth='34563:ABCDEFG', chat_id='123456', body='message',
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
# TESTS: TelegramBot.__str__
##############################################################################

def test_tgram_str(get_tgram, capsys):
    """
    GIVEN t=TelegramBot()
    WHEN print(t)
    THEN assert proper output prints
    """
    t = get_tgram
    t.from_ = 'Me'
    t.to = 'You'
    t.subject = 'Chat'
    print(t)
    out, err = capsys.readouterr()
    assert 'From: Me' in out
    assert 'To: You' in out
    assert 'Chat ID: 123456' in out
    assert 'Subject: Chat' in out
    assert 'Body: message' in out
    assert 'Attachments: [\'https://url1.com\', \'https://url2.com\']' in out
    assert '' in err


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

def test_tgram_send_content_verbose_false(get_tgram, capsys, mocker):
    """
    GIVEN a valid TelegramBot object
    WHEN send_content() is called with verbose=False
    THEN assert the proper send sequence occurs
    """
    req_mock = mocker.patch.object(requests, 'post')
    req_mock.return_value.status_code = 200
    t = get_tgram
    t.send_content()
    out, err = capsys.readouterr()
    assert req_mock.call_count == 1
    assert out == ''
    assert err == ''


def test_tgram_send_content_msgBody_verbose_true(get_tgram, capsys, mocker):
    """
    GIVEN a valid TelegramBot object
    WHEN send_content() is called with verbose=True
    THEN assert the proper send sequence occurs
    """
    req_mock = mocker.patch.object(requests, 'post')
    req_mock.return_value.status_code = 200
    t = get_tgram
    t.verbose = True
    t.send_content()
    out, err = capsys.readouterr()
    assert req_mock.call_count == 1
    assert 'Message body sent' in out
    assert 'Attachment: https://url1.com' not in out
    assert 'Attachment: https://url2.com' not in out
    assert err == ''


def test_tgram_send_content_attachments_verbose_true(get_tgram, capsys, mocker):
    """
    GIVEN a valid TelegramBot object
    WHEN send_content() is called with verbose=True
    THEN assert the proper send sequence occurs
    """
    req_mock = mocker.patch.object(requests, 'post')
    req_mock.return_value.status_code = 200
    t = get_tgram
    t.verbose = True
    t.message['document'] = 'https://url1.com'
    t.send_content(method='/sendDocument')
    out, err = capsys.readouterr()
    assert req_mock.call_count == 1
    assert 'Message body sent' not in out
    assert 'Attachment: https://url1.com' in out
    assert err == ''


def test_tgram_send_content_statusGT300_verbose_true(get_tgram, capsys, mocker):
    """
    GIVEN a valid TelegramBot object
    WHEN send_content() is called but an error occurs, status_code > 300, verbose=True
    THEN assert the proper send sequence occurs
    """
    req_mock = mocker.patch.object(requests, 'post')
    req_mock.return_value.status_code = 403
    req_mock.return_value.text = 'test error'
    t = get_tgram
    t.verbose = True
    t.send_content()
    out, err = capsys.readouterr()
    assert req_mock.call_count == 1
    assert 'Error while sending Message body' in out
    assert 'test error' in out
    assert err == ''

##############################################################################
# TESTS: TelegramBot.send
##############################################################################

def test_send_verbose_false(get_tgram, mocker, capsys):
    """
    GIVEN a TelegramBot instance
    WHEN send() is called with verbose=False
    THEN assert correct sequence is called and correct output printed
    """
    con_mock = mocker.patch.object(TelegramBot, 'construct_message')
    send_cont_mock = mocker.patch.object(TelegramBot, 'send_content')
    t = get_tgram
    t.send()
    out, err = capsys.readouterr()
    assert con_mock.call_count == 1
    assert send_cont_mock.call_count == 3
    assert 'Message sent.' in out
    assert 'Debugging info' not in out


def test_send_verbose_true(get_tgram, mocker, capsys):
    """
    GIVEN a TelegramBot instance
    WHEN send() is called with verbose=True
    THEN assert correct sequence is called and correct output printed
    """
    con_mock = mocker.patch.object(TelegramBot, 'construct_message')
    send_cont_mock = mocker.patch.object(TelegramBot, 'send_content')
    t = get_tgram
    t.verbose = True
    t.send()
    out, err = capsys.readouterr()
    assert con_mock.call_count == 1
    assert send_cont_mock.call_count == 3
    assert 'Message sent.' in out
    assert 'Debugging info' in out


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
