"""
Module designed to make creating and sending chat messages easy.

1.  SlackWebHook
    - Send messages via the Incoming Webhooks feature
    - https://api.slack.com/incoming-webhooks
"""

import json
import urllib
from collections import deque

import attr
from attr.validators import instance_of

from ._interface import Message
from .eventloop import MESSAGELOOP


@attr.s
class SlackWebHook(Message):
    """
    Create and send Slack message via the Incoming WebHooks API.

    Args:
        webhook_url: str, webhook url for installed slack app.
        text: str, message to send.
        attach_urls: str or list, each item is a url to attach

    Usage:
        Create a SlackWebHook object with required Args above.
        Send message with self.send() or self.send_async() methods.

    Note:
        For API description:
        https://api.slack.com/incoming-webhooks
    """

    webhook_url = attr.ib(validator=instance_of(str))
    text = attr.ib(validator=instance_of(str))
    attach_urls = attr.ib()
    message = {}
    sent_messages = deque()


    def construct_message(self):
        """Build the message params."""
        self.message['text'] = self.text
        self.add_attachments()
        headers = {'Content-Type': 'application/json'}
        req = urllib.request.Request(self.webhook_url, headers=headers,
                                     data=json.dumps(self.message).encode())
        return req


    def add_attachments(self):
        """Add attachments."""
        if self.attach_urls:
            if not isinstance(self.attach_urls, list):
                self.attach_urls = [self.attach_urls]

            self.message['attachments'] = [{'image_url': url, 'author_name': ''}
                                           for url in self.attach_urls]


    def send(self):
        """
        Send the message via HTTP POST.
        Uses the urllib standard library since 'requests' is not yet
        compatible with gevent, which is used in the eventloop.
        """
        req = self.construct_message()
        resp = urllib.request.urlopen(req)

        print('Message sent...')
        self.sent_messages.append(repr(self))


    def send_async(self):
        """Send message asynchronously."""
        MESSAGELOOP.add_message(self)
