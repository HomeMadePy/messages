"""messages.slack tests."""

import pytest
import requests

import messages.slack
from messages.slack import SlackWebhook
from messages.slack import SlackPost
from messages._eventloop import MESSAGELOOP


##############################################################################
# FIXTURES
##############################################################################

@pytest.fixture()
def get_slackWH(cfg_mock, mocker):
    """Return a valid SlackWebhook object."""
    mocker.patch.object(messages.slack, 'check_config_file')
    return SlackWebhook(auth='https://testurl.com', body='message',
            attachments=['https://url1.com', 'https://url2.com'],
            profile='myProfile')


@pytest.fixture()
def get_slackP(cfg_mock, mocker):
    """Return a valid SlackPost object."""
    mocker.patch.object(messages.slack, 'check_config_file')
    return SlackPost(auth='1234:ABCD', channel='general',
            body='message', attachments=['https://url1.com', 'https://url2.com'],
            profile='myProfile')


##############################################################################
# TESTS: Slack*.__init__
##############################################################################

def test_slackWH_init(get_slackWH):
    """
    GIVEN a need for a SlackWebhook object
    WHEN instantiated
    THEN assert it is properly created
    """
    s = get_slackWH
    assert s.body == 'message'
    assert isinstance(s.message, dict)


def test_slackP_init(get_slackP):
    """
    GIVEN a need for a SlackPost object
    WHEN instantiated
    THEN assert it is properly created
    """
    s = get_slackP
    assert s.body == 'message'
    assert isinstance(s.message, dict)


##############################################################################
# TESTS: Slack*.__str__
##############################################################################

def test_slackWH_str(get_slackWH, capsys):
    """
    GIVEN a SlackWebhook object
    WHEN print() is called on the object
    THEN assert the proper output prints
    """
    s = get_slackWH
    print(s)
    out, err = capsys.readouterr()
    assert "['https://url1.com', 'https://url2.com']" in out
    assert "'message'" in out
    assert err == ''


def test_slackP_str(get_slackP, capsys):
    """
    GIVEN a SlackPost object
    WHEN print() is called on the object
    THEN assert the proper output prints
    """
    s = get_slackP
    print(s)
    out, err = capsys.readouterr()
    assert "['https://url1.com', 'https://url2.com']" in out
    assert "'message'" in out
    assert 'gener' in out
    assert err == ''


##############################################################################
# TESTS: Slack*.construct_message
##############################################################################

def test_slackWH_construct_message(get_slackWH, mocker):
    """
    GIVEN a valid SlackWebhook object
    WHEN construct_message() is called
    THEN assert the message is properly created
    """
    add_mock = mocker.patch.object(SlackWebhook, 'add_attachments')
    s = get_slackWH
    s.construct_message()
    assert s.message['text'] == 'message'
    assert add_mock.call_count == 1


def test_slackP_construct_message(get_slackP, mocker):
    """
    GIVEN a valid SlackPost object
    WHEN construct_message() is called
    THEN assert the message is properly created
    """
    add_mock = mocker.patch.object(SlackPost, 'add_attachments')
    s = get_slackP
    s.construct_message()
    assert s.message['text'] == 'message'
    assert add_mock.call_count == 1


def test_slackWH_construct_message_withFromSubj(get_slackWH, mocker):
    """
    GIVEN a valid SlackWebhook object
    WHEN construct_message() is called
    THEN assert the message is properly created
    """
    add_mock = mocker.patch.object(SlackWebhook, 'add_attachments')
    s = get_slackWH
    s.from_ = 'me'
    s.subject = 'Tst Msg'
    s.construct_message()
    expected = 'From: me\nSubject: Tst Msg\nmessage'
    assert s.message['text'] == expected
    assert add_mock.call_count == 1


def test_slackP_construct_message_withFromSubj(get_slackP, mocker):
    """
    GIVEN a valid SlackPost object
    WHEN construct_message() is called
    THEN assert the message is properly created
    """
    add_mock = mocker.patch.object(SlackPost, 'add_attachments')
    s = get_slackP
    s.from_ = 'me'
    s.subject = 'Tst Msg'
    s.construct_message()
    expected = 'From: me\nSubject: Tst Msg\nmessage'
    assert s.message['text'] == expected
    assert add_mock.call_count == 1


##############################################################################
# TESTS: Slack*.add_attachments
##############################################################################

def test_slackWH_add_attachments_list(get_slackWH):
    """
    GIVEN a valid SlackWebhook object with self.attach_urls = list
    WHEN add_attachments() is called
    THEN assert the urls are properly attached to the message
    """
    s = get_slackWH
    s.add_attachments()
    expected = [{'image_url': 'https://url1.com', 'author_name': ''},
                {'image_url': 'https://url2.com', 'author_name': ''}]
    assert s.message['attachments'] == expected


def test_slackP_add_attachments_list(get_slackP):
    """
    GIVEN a valid SlackPost object with self.attach_urls = list
    WHEN add_attachments() is called
    THEN assert the urls are properly attached to the message
    """
    s = get_slackP
    s.add_attachments()
    expected = [{'image_url': 'https://url1.com', 'author_name': ''},
                {'image_url': 'https://url2.com', 'author_name': ''}]
    assert s.message['attachments'] == expected


def test_slackWH_add_attachments_str(get_slackWH):
    """
    GIVEN a valid SlackWebhook object with self.attach_urls = str
    WHEN add_attachments() is called
    THEN assert the urls are properly attached to the message
    """
    s = get_slackWH
    s.attachments = 'https://url1.com'
    s.add_attachments()
    expected = [{'image_url': 'https://url1.com', 'author_name': ''}]
    assert s.message['attachments'] == expected


def test_slackP_add_attachments_str(get_slackP):
    """
    GIVEN a valid SlackPost object with self.attach_urls = str
    WHEN add_attachments() is called
    THEN assert the urls are properly attached to the message
    """
    s = get_slackP
    s.attachments = 'https://url1.com'
    s.add_attachments()
    expected = [{'image_url': 'https://url1.com', 'author_name': ''}]
    assert s.message['attachments'] == expected


def test_slackWH_add_attachments_with_params(get_slackWH):
    """
    GIVEN a valid SlackWebhook object with extra attachment params
    WHEN add_attachments() is called
    THEN assert the extra params are properly added
    """
    s = get_slackWH
    s.attachments = 'https://url1.com'
    s.params = {'author_name': 'me', 'text': 'image of me'}
    s.add_attachments()
    expected = [{'image_url': 'https://url1.com', 'author_name': 'me',
                'text': 'image of me'}]
    assert s.message['attachments'] == expected


def test_slackP_add_attachments_with_params(get_slackP):
    """
    GIVEN a valid SlackPost object with extra attachment params
    WHEN add_attachments() is called
    THEN assert the extra params are properly added
    """
    s = get_slackP
    s.attachments = 'https://url1.com'
    s.params = {'author_name': 'me', 'text': 'image of me'}
    s.add_attachments()
    expected = [{'image_url': 'https://url1.com', 'author_name': 'me',
                'text': 'image of me'}]
    assert s.message['attachments'] == expected


##############################################################################
# TESTS: Slack*.send
##############################################################################

def test_slackWH_send(get_slackWH, capsys, mocker):
    """
    GIVEN a valid SlackWebhook object
    WHEN send() is called
    THEN assert the proper send sequence occurs
    """
    con_mock = mocker.patch.object(SlackWebhook, 'construct_message')
    req_mock = mocker.patch.object(requests, 'post')
    s = get_slackWH
    s.send()
    out, err = capsys.readouterr()
    assert con_mock.call_count == 1
    assert req_mock.call_count == 1
    assert out == 'Message sent.\n'
    assert err == ''


def test_slackP_send(get_slackP, capsys, mocker):
    """
    GIVEN a valid SlackPost object
    WHEN send() is called
    THEN assert the proper send sequence occurs
    """
    con_mock = mocker.patch.object(SlackPost, 'construct_message')
    req_mock = mocker.patch.object(requests, 'post')
    s = get_slackP
    s.send()
    out, err = capsys.readouterr()
    assert con_mock.call_count == 1
    assert req_mock.call_count == 1
    assert out == 'Message sent.\n'
    assert err == ''


def test_slackWH_send_verbose_true(get_slackWH, capsys, mocker):
    """
    GIVEN a valid SlackWebhook object
    WHEN *.send() is called
    THEN assert the correct functions are called, correct attributes
        updated and correct debug output is generated (using verbose flag
        set to True)
    """
    con_mock = mocker.patch.object(SlackWebhook, 'construct_message')
    req_mock = mocker.patch.object(requests, 'post')
    s = get_slackWH
    s.verbose = True
    s.send()
    out, err = capsys.readouterr()
    assert 'Debugging info' in out
    assert 'Message created.' in out
    assert ' * URL: https://testurl.com' in out
    assert ' * From: Not Specified' in out
    assert ' * Subject: None' in out
    assert ' * Body: \'message\'' in out
    assert ' * Attachments: [\'https://url1.com\', \'https://url2.com\']' in out
    assert 'Message sent.' in out
    assert err == ''


def test_slackWH_send_verbose_false(get_slackWH, capsys, mocker):
    """
    GIVEN a valid SlackWebhook object
    WHEN *.send() is called
    THEN assert the correct functions are called, correct attributes
        updated and correct debug output is generated (using verbose flag
        set to False)
    """
    con_mock = mocker.patch.object(SlackWebhook, 'construct_message')
    req_mock = mocker.patch.object(requests, 'post')
    s = get_slackWH
    s.verbose = False
    s.send()
    out, err = capsys.readouterr()
    assert 'Debugging info' not in out
    assert 'Message created.' not in out
    assert ' * URL: https://test_url.com' not in out
    assert ' * From: Not Specified' not in out
    assert ' * Subject: None' not in out
    assert ' * Body: \'message\'' not in out
    assert ' * Attachments: [\'https://url1.com\', \'https://url2.com\']' not in out
    assert 'Message sent.' in out
    assert err == ''


def test_slackP_send_verbose_true(get_slackP, capsys, mocker):
    """
    GIVEN a valid SlackPost object
    WHEN *.send() is called
    THEN assert the correct functions are called, correct attributes
        updated and correct debug output is generated (using verbose flag
        set to True)
    """
    con_mock = mocker.patch.object(SlackPost, 'construct_message')
    req_mock = mocker.patch.object(requests, 'post')
    s = get_slackP
    s.verbose = True
    s.send()
    out, err = capsys.readouterr()
    assert 'Debugging info' in out
    assert 'Message created.' in out
    assert ' * Channel: general' in out
    assert ' * From: Not Specified' in out
    assert ' * Subject: None' in out
    assert ' * Body: \'message\'' in out
    assert ' * Attachments: [\'https://url1.com\', \'https://url2.com\']' in out
    assert 'Message sent.' in out
    assert err == ''


def test_slackP_send_verbose_false(get_slackP, capsys, mocker):
    """
    GIVEN a valid SlackPost object
    WHEN *.send() is called
    THEN assert the correct functions are called, correct attributes
        updated and correct debug output is generated (using verbose flag
        set to False)
    """
    con_mock = mocker.patch.object(SlackPost, 'construct_message')
    req_mock = mocker.patch.object(requests, 'post')
    s = get_slackP
    s.verbose = False
    s.send()
    out, err = capsys.readouterr()
    assert 'Debugging info' not in out
    assert 'Message created.' not in out
    assert ' * Channel: general' not in out
    assert ' * From: Not Specified' not in out
    assert ' * Subject: None' not in out
    assert ' * Body: \'message\'' not in out
    assert ' * Attachments: [\'https://url1.com\', \'https://url2.com\']' not in out
    assert 'Message sent.' in out
    assert err == ''

##############################################################################
# TESTS: Slack*.send_async
##############################################################################

def test_slackWH_send_async(get_slackWH, mocker):
    """
    GIVEN a valid SlackWebhook object
    WHEN send_async() is called
    THEN assert the proper send sequence occurs
    """
    msgloop_mock = mocker.patch.object(MESSAGELOOP, 'add_message')
    s = get_slackWH
    s.send_async()
    assert msgloop_mock.call_count == 1


def test_slackP_send_async(get_slackP, mocker):
    """
    GIVEN a valid SlackPost object
    WHEN send_async() is called
    THEN assert the proper send sequence occurs
    """
    msgloop_mock = mocker.patch.object(MESSAGELOOP, 'add_message')
    s = get_slackP
    s.send_async()
    assert msgloop_mock.call_count == 1
