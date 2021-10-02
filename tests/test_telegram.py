"""messages.slack tests."""

import pytest
import httpx

import messages.telegram
from messages.telegram import TelegramBot
from messages._exceptions import MessageSendError


##############################################################################
# FIXTURES
##############################################################################

@pytest.fixture()
def get_tgram():
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
    assert t.auth == '***obfuscated***'
    assert '_auth' in t.__dict__
    assert t._auth == '34563:ABCDEFG'
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
    assert 'Body: \'message\'' in out
    assert 'Attachments: [\'https://url1.com\', \'https://url2.com\']' in out
    assert '' in err


##############################################################################
# TESTS: TelegramBot.get_chat_id
##############################################################################

def test_tgram_getChatID(get_tgram, httpx_mock):
    """
    GIVEN a TelegramBot instance with unknown chat_id of recipient
    WHEN get_chat_id() is called
    THEN assert proper data is returned

    httpx_mock is a built-in fixture from pytest-httpx
    """
    json_response = {'result': [{'message':{
        'from':{'username': 'YOU', 'id': '123456'}}}]}
    httpx_mock.add_response(json=json_response, status_code=201)
    t = get_tgram
    id = t.get_chat_id('@YOU')
    assert id == '123456'


##############################################################################
# TESTS: TelegramBot._construct_message
##############################################################################

def test_tgram_construct_message(get_tgram):
    """
    GIVEN a valid TelegramBot object
    WHEN construct_message() is called
    THEN assert the message is properly created
    """
    t = get_tgram
    t._construct_message()
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
    t._construct_message()
    expected = 'From: me\n' + 'Subject: this is a test\n' + 'message'
    assert t.message['text'] == expected


##############################################################################
# TESTS: TelegramBot._send_content
##############################################################################

def test_tgram_send_content_verbose_false(get_tgram, capsys, httpx_mock):
    """
    GIVEN a valid TelegramBot object
    WHEN _send_content() is called with verbose=False
    THEN assert the proper send sequence occurs

    httpx_mock is a built-in fixture from pytest-httpx
    """
    httpx_mock.add_response(status_code=201)
    t = get_tgram
    t._send_content()
    out, err = capsys.readouterr()
    assert out == ''
    assert err == ''


def test_tgram_send_content_msgBody_verbose_true(get_tgram, capsys, httpx_mock):
    """
    GIVEN a valid TelegramBot object
    WHEN _send_content() is called with verbose=True
    THEN assert the proper send sequence occurs

    httpx_mock is a built-in fixture from pytest-httpx
    """
    httpx_mock.add_response(status_code=201)
    t = get_tgram
    t.verbose = True
    t._send_content()
    out, err = capsys.readouterr()
    assert 'Message body sent' in out
    assert 'Attachment: https://url1.com' not in out
    assert 'Attachment: https://url2.com' not in out
    assert err == ''


def test_tgram_send_content_attachments_verbose_true_list(get_tgram, capsys, httpx_mock):
    """
    GIVEN a valid TelegramBot object
    WHEN _send_content() is called with verbose=True
    THEN assert the proper send sequence occurs

    httpx_mock is a built-in fixture from pytest-httpx
    """
    httpx_mock.add_response(status_code=201)
    t = get_tgram
    t.verbose = True
    t.message['document'] = 'https://url1.com'
    t._send_content(method='/sendDocument')
    out, err = capsys.readouterr()
    assert 'Message body sent' not in out
    assert 'Attachment: https://url1.com' in out
    assert err == ''


def test_tgram_send_content_raisesMessSendErr(get_tgram, httpx_mock):
    """
    GIVEN a valid TelegramBot object
    WHEN _send_content() is called but an http error occurs
    THEN assert MessageSendError is raised

    httpx_mock is a built-in fixture from pytest-httpx
    """
    httpx_mock.add_response(status_code=404)
    t = get_tgram
    with pytest.raises(MessageSendError):
        t._send_content()


##############################################################################
# TESTS: TelegramBot.send
##############################################################################

def test_tgram_send_verbose_false(get_tgram, mocker, capsys):
    """
    GIVEN a TelegramBot instance
    WHEN send() is called with verbose=False
    THEN assert correct sequence is called and correct output printed
    """
    con_mock = mocker.patch.object(TelegramBot, '_construct_message')
    send_cont_mock = mocker.patch.object(TelegramBot, '_send_content')
    t = get_tgram
    t.send()
    out, err = capsys.readouterr()
    assert con_mock.call_count == 1
    assert send_cont_mock.call_count == 3
    assert 'Message sent.' in out
    assert 'Debugging info' not in out


def test_tgram_send_verbose_true(get_tgram, mocker, capsys):
    """
    GIVEN a TelegramBot instance
    WHEN send() is called with verbose=True
    THEN assert correct sequence is called and correct output printed
    """
    con_mock = mocker.patch.object(TelegramBot, '_construct_message')
    send_cont_mock = mocker.patch.object(TelegramBot, '_send_content')
    t = get_tgram
    t.verbose = True
    t.send()
    out, err = capsys.readouterr()
    assert con_mock.call_count == 1
    assert send_cont_mock.call_count == 3
    assert 'Message sent.' in out


def test_tgram_send_attachmentStr(get_tgram, mocker, capsys):
    """
    GIVEN a TelegramBot instance
    WHEN send() is called with verbose=True and an attachment as a string
        instead of list of strings
    THEN assert correct sequence is called and correct output printed
    """
    con_mock = mocker.patch.object(TelegramBot, '_construct_message')
    send_cont_mock = mocker.patch.object(TelegramBot, '_send_content')
    t = get_tgram
    t.attachments = t.attachments[0]
    t.verbose = True
    t.send()
    out, err = capsys.readouterr()
    assert con_mock.call_count == 1
    assert send_cont_mock.call_count == 2
    assert 'Message sent.' in out


##############################################################################
# TESTS: TelegramBot._send_content_async
##############################################################################

@pytest.mark.asyncio
async def test_tgram_send_content_async(get_tgram, capsys, httpx_mock):
    """
    GIVEN a valid TelegramBot object
    WHEN _send_content_async() is called
    THEN assert the proper send sequence occurs

    httpx_mock is a built-in fixture from pytest-httpx
    """
    httpx_mock.add_response(status_code=201)
    t = get_tgram
    await t._send_content_async()
    out, err = capsys.readouterr()
    assert out == ''
    assert err == ''


@pytest.mark.asyncio
async def test_tgram_send_content_async_attachments_list(get_tgram, capsys, httpx_mock):
    """
    GIVEN a valid TelegramBot object
    WHEN _send_content_async() is called
    THEN assert the proper send sequence occurs

    httpx_mock is a built-in fixture from pytest-httpx
    """
    httpx_mock.add_response(status_code=201)
    t = get_tgram
    t.verbose = True
    t.message['document'] = 'https://url1.com'
    await t._send_content_async(method='/sendDocument')
    out, err = capsys.readouterr()
    assert err == ''


@pytest.mark.asyncio
async def test_tgram_send_content_async_raisesMessSendErr(get_tgram, httpx_mock):
    """
    GIVEN a valid TelegramBot object
    WHEN _send_content_async() is called but an http error occurs
    THEN assert MessageSendError is raised

    httpx_mock is a built-in fixture from pytest-httpx
    """
    httpx_mock.add_response(status_code=404)
    t = get_tgram
    with pytest.raises(MessageSendError):
        await t._send_content_async()


##############################################################################
# TESTS: TelegramBot.send_async
##############################################################################

@pytest.mark.asyncio
async def test_tgram_send_async(get_tgram, mocker, capsys, httpx_mock):
    """
    GIVEN a TelegramBot instance
    WHEN send_async() is called
    THEN assert correct sequence is called
    """
    con_mock = mocker.patch.object(TelegramBot, '_construct_message')
    httpx_mock.add_response(status_code=201)
    t = get_tgram
    await t.send_async()
    out, err = capsys.readouterr()
    assert err == ''


@pytest.mark.asyncio
async def test_tgram_send_async_attachmentStr(get_tgram, mocker, capsys, httpx_mock):
    """
    GIVEN a TelegramBot instance
    WHEN send_async() is called with attachments as a string
        instead of list of strings
    THEN assert correct sequence is called
    """
    con_mock = mocker.patch.object(TelegramBot, '_construct_message')
    httpx_mock.add_response(status_code=201)
    t = get_tgram
    t.attachments = t.attachments[0]
    await t.send_async()
    out, err = capsys.readouterr()
    assert err == ''
