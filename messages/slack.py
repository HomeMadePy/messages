"""
Module designed to make creating and sending chat messages easy.

1.  SlackWebhook
    - Send messages via the Incoming Webhooks feature
    - https://api.slack.com/incoming-webhooks
"""

from collections import deque

import requests

from .config import configure
from ._eventloop import MESSAGELOOP
from ._interface import Message


class SlackWebhook(Message):
    """
    Create and send Slack message via the Incoming WebHooks API.

    Args:
        :from_: (str) optional arg to specify who message is from.
        :url: (str) webhook url for installed slack app.
        :subject: (str) optional arg to specify message subject.
        :body: (str) message to send.
        :attachments: (str or list) each item is a url to attach
        :params: (dict) additional attributes to add to each attachment,
            i.e. author_name, title, text, etc., see API for information
            on which attributes are possible.
        :profile: (str) use a separate account profile specified by name
        :save: (bool) save pertinent values in the messages config file,
            such as from_, url (encrypted keyring) to make
            sending messages faster.

    Attributes:
        :message: (dict) current form of the message to be constructed
        :sent_messages: (deque) all messages sent with current SlackWebhook
            object, acting as a log of messages sent in the current session.

    Usage:
        Create a SlackWebhook object with required Args above.
        Send message with self.send() or self.send_async() methods.

    Note:
        For API description:
        https://api.slack.com/incoming-webhooks
    """

    def __init__(
        self, from_=None, url=None, subject=None, body='', attachments=None,
        params=None, profile=None, save=False
    ):

        config_kwargs = {'from_': from_, 'url': url, 'profile': profile,
                'save': save}

        configure(self, params=config_kwargs,
                to_save={'from_', 'url'}, credentials={})

        self.subject = subject
        self.body = body
        self.attachments = attachments
        self.params = params
        self.message = {}
        self.sent_messages = deque()


    def construct_message(self):
        """Build the message params."""
        self.message['text'] = ''
        if self.from_:
            self.message['text'] += ('From: ' + self.from_ + '\n')
        if self.subject:
            self.message['text'] += ('Subject: ' + self.subject + '\n')

        self.message['text'] += self.body
        self.add_attachments()


    def add_attachments(self):
        """Add attachments."""
        if self.attachments:
            if not isinstance(self.attachments, list):
                self.attachments = [self.attachments]

            self.message['attachments'] = [{'image_url': url,
                                            'author_name': ''}
                                           for url in self.attachments]
            if self.params:
                for attachment in self.message['attachments']:
                    attachment.update(self.params)


    def send(self):
        """Send the message via HTTP POST."""
        self.construct_message()
        requests.post(self.url, json=self.message)
        print('Message sent...')
        self.sent_messages.append(repr(self))


    def send_async(self):
        """Send message asynchronously."""
        MESSAGELOOP.add_message(self)
