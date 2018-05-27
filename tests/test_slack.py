"""messages.slack tests."""

import pytest
import requests

from collections import deque

from messages.slack import SlackWebhook
from messages._eventloop import MESSAGELOOP


##############################################################################
# FIXTURES
##############################################################################

@pytest.fixture()
def get_slack(cfg_mock):
    """Return a valid SlackWebhook object."""
    return SlackWebhook(url='https://test_url.com', body='message',
                attachments=['https://url1.com', 'https://url2.com'])


##############################################################################
# TESTS: SlackWebhook.__init__
##############################################################################

def test_slack_init(get_slack):
    """
    GIVEN a need for a SlackWebhook object
    WHEN instantiated
    THEN assert it is properly created
    """
    s = get_slack
    assert s.body == 'message'
    assert isinstance(s.message, dict)
    assert isinstance(s.sent_messages, deque)


##############################################################################
# TESTS: SlackWebhook.construct_message
##############################################################################

def test_slack_construct_message(get_slack, mocker):
    """
    GIVEN a valid SlackWebhook object
    WHEN construct_message() is called
    THEN assert the message is properly created
    """
    add_mock = mocker.patch.object(SlackWebhook, 'add_attachments')
    s = get_slack
    s.construct_message()
    assert s.message['text'] == 'message'
    assert add_mock.call_count == 1


def test_slack_construct_message_withFromSubj(get_slack, mocker):
    """
    GIVEN a valid SlackWebhook object
    WHEN construct_message() is called
    THEN assert the message is properly created
    """
    add_mock = mocker.patch.object(SlackWebhook, 'add_attachments')
    s = get_slack
    s.from_ = 'me'
    s.subject = 'Tst Msg'
    s.construct_message()
    expected = 'From: me\nSubject: Tst Msg\nmessage'
    assert s.message['text'] == expected
    assert add_mock.call_count == 1


##############################################################################
# TESTS: SlackWebhook.add_attachments
##############################################################################

def test_slack_add_attachments_list(get_slack):
    """
    GIVEN a valid SlackWebhook object with self.attach_urls = list
    WHEN add_attachments() is called
    THEN assert the urls are properly attached to the message
    """
    s = get_slack
    s.add_attachments()
    expected = [{'image_url': 'https://url1.com', 'author_name': ''},
                {'image_url': 'https://url2.com', 'author_name': ''}]
    assert s.message['attachments'] == expected


def test_slack_add_attachments_str(get_slack):
    """
    GIVEN a valid SlackWebhook object with self.attach_urls = str
    WHEN add_attachments() is called
    THEN assert the urls are properly attached to the message
    """
    s = get_slack
    s.attachments = 'https://url1.com'
    s.add_attachments()
    expected = [{'image_url': 'https://url1.com', 'author_name': ''}]
    assert s.message['attachments'] == expected


def test_slack_add_attachments_with_params(get_slack):
    """
    GIVEN a valid SlackWebhook object with extra attachment params
    WHEN add_attachments() is called
    THEN assert the extra params are properly added
    """
    s = get_slack
    s.attachments = 'https://url1.com'
    s.params = {'author_name': 'me', 'text': 'image of me'}
    s.add_attachments()
    expected = [{'image_url': 'https://url1.com', 'author_name': 'me',
                'text': 'image of me'}]
    assert s.message['attachments'] == expected


##############################################################################
# TESTS: SlackWebhook.send
##############################################################################

def test_slack_send(get_slack, capsys, mocker):
    """
    GIVEN a valid SlackWebhook object
    WHEN send() is called
    THEN assert the proper send sequence occurs
    """
    con_mock = mocker.patch.object(SlackWebhook, 'construct_message')
    req_mock = mocker.patch.object(requests, 'post')
    s = get_slack
    s.send()
    out, err = capsys.readouterr()
    assert con_mock.call_count == 1
    assert req_mock.call_count == 1
    assert out == 'Message sent...\n'
    assert err == ''
    assert len(s.sent_messages) == 1


##############################################################################
# TESTS: SlackWebhook.send_async
##############################################################################

def test_slack_send_async(get_slack, mocker):
    """
    GIVEN a valid SlackWebhook object
    WHEN send_async() is called
    THEN assert the proper send sequence occurs
    """
    msgloop_mock = mocker.patch.object(MESSAGELOOP, 'add_message')
    s = get_slack
    s.send_async()
    assert msgloop_mock.call_count == 1
