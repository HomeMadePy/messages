"""messages.slack tests."""

import pytest

import requests

from collections import deque
from unittest.mock import patch

from messages.slack import SlackWebhook
from messages._eventloop import MESSAGELOOP


##############################################################################
# FIXTURES
##############################################################################

@pytest.fixture()
def get_slack(cfg_mock):
    """Return a valid SlackWebhook object."""
    return SlackWebhook(url='test_url', body='message',
                attachments=['url1', 'url2'])


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
    assert s.url == 'test_url'
    assert s.body == 'message'
    assert s.attachments == ['url1', 'url2']
    assert isinstance(s.message, dict)
    assert isinstance(s.sent_messages, deque)


##############################################################################
# TESTS: SlackWebhook.construct_message
##############################################################################

@patch.object(SlackWebhook, 'add_attachments')
def test_slack_construct_message(add_mock, get_slack):
    """
    GIVEN a valid SlackWebhook object
    WHEN construct_message() is called
    THEN assert the message is properly created
    """
    s = get_slack
    s.construct_message()
    assert s.message['text'] == 'message'
    assert add_mock.call_count == 1


@patch.object(SlackWebhook, 'add_attachments')
def test_slack_construct_message_withFromSubj(add_mock, get_slack):
    """
    GIVEN a valid SlackWebhook object
    WHEN construct_message() is called
    THEN assert the message is properly created
    """
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
    expected = [{'image_url': 'url1', 'author_name': ''},
                {'image_url': 'url2', 'author_name': ''}]
    assert s.message['attachments'] == expected


def test_slack_add_attachments_str(get_slack):
    """
    GIVEN a valid SlackWebhook object with self.attach_urls = str
    WHEN add_attachments() is called
    THEN assert the urls are properly attached to the message
    """
    s = get_slack
    s.attachments = 'url1'
    s.add_attachments()
    expected = [{'image_url': 'url1', 'author_name': ''}]
    assert s.message['attachments'] == expected


def test_slack_add_attachments_with_params(get_slack):
    """
    GIVEN a valid SlackWebhook object with extra attachment params
    WHEN add_attachments() is called
    THEN assert the extra params are properly added
    """
    s = get_slack
    s.attachments = 'url1'
    s.params = {'author_name': 'me', 'text': 'image of me'}
    s.add_attachments()
    expected = [{'image_url': 'url1', 'author_name': 'me',
                'text': 'image of me'}]
    assert s.message['attachments'] == expected


##############################################################################
# TESTS: SlackWebhook.send
##############################################################################

@patch.object(requests, 'post')
@patch.object(SlackWebhook, 'construct_message')
def test_slack_send(con_mock, req_mock, get_slack, capsys):
    """
    GIVEN a valid SlackWebhook object
    WHEN send() is called
    THEN assert the proper send sequence occurs
    """
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

@patch.object(MESSAGELOOP, 'add_message')
def test_slack_send_async(msgloop_mock, get_slack):
    """
    GIVEN a valid SlackWebhook object
    WHEN send_async() is called
    THEN assert the proper send sequence occurs
    """
    s = get_slack
    s.send_async()
    assert msgloop_mock.call_count == 1
