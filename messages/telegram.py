"""
Module designed to make creating and sending chat messages easy.

1.  TelegramBot
    - Send messages via the Telegram Bot feature
    - https://core.telegram.org/bots
"""

import sys

import requests

from ._config import configure
from ._eventloop import MESSAGELOOP
from ._interface import Message


class TelegramBot(Message):
    """
    Create and send Telegram message via the Telegram Bot API.

    Args:
        :from_: (str) optional arg to specify who message is from.
        :bot_token: (str) auth token for bot.
        :chat_id: (str) chat_id for already-intiated chat.  Integer represented
            as a string.  Recipient must have already initiated chat at some
            point in the past for bot to send message.
        :user_name: (str) if chat_id is unknown, can specify username of
            recipient to lookup via API call.
        :subject: (str) optional arg to specify message subject.
        :body: (str) message to send.
        :attachments: (str or list) each item is a url to attach
        :params: (dict) additional attributes to add to message,
            i.e. parse_mode (HTML or Markdown, see API for information
            on which attributes are possible.
        :profile: (str) use a separate account profile specified by name
        :save: (bool) save pertinent values in the messages config file,
            such as from_, chat_id, bot_token (encrypted keyring) to make
            sending messages faster.

    Attributes:
        :message: (dict) current form of the message to be constructed

    Usage:
        Create a TelegramBot object with required Args above.
        Send message with self.send() or self.send_async() methods.

    Note:
        For API description:
        https://core.telegram.org/bots/api#available-methods
    """

    def __init__(
        self, from_=None, bot_token=None, chat_id=None, username=None,
        subject=None, body='', attachments=None, params=None, profile=None,
        save=False
    ):

        config_kwargs = {'from_': from_, 'bot_token': bot_token,
                     'chat_id': chat_id or self.get_chat_id(username),
                     'profile': profile, 'save': save}

        configure(self, params=config_kwargs,
                to_save={'from_', 'chat_id'}, credentials={'bot_token'})

        self.username = username
        self.subject = subject
        self.body = body
        self.attachments = attachments or []
        self.params = params or {}
        self.base_url = 'https://api.telegram.org/bot' + self.bot_token
        self.message = {}


    def get_chat_id(self, username):
        """Lookup chat_id of username if chat_id is unknown via API call."""
        if username is not None:
            chats = requests.get(self.base_url + '/getUpdates').json()
            user = username.split('@')[-1]
            for chat in chats['result']:
                if chat['message']['from']['username'] == user:
                    return chat['message']['from']['id']


    def construct_message(self):
        """Build the message params."""
        self.message['chat_id'] = self.chat_id
        self.message['text'] = ''
        if self.from_:
            self.message['text'] += ('From: ' + self.from_ + '\n')
        if self.subject:
            self.message['text'] += ('Subject: ' + self.subject + '\n')

        self.message['text'] += self.body
        self.message.update(self.params)


    def send_content(self, method='/sendMessage'):
        """send via HTTP Post."""
        url = self.base_url + method
        r = requests.post(url, json=self.message)

        if r.status_code == 200:
            print('Message sent...', file=sys.stdout)
        if r.status_code > 300:
            print('Error while sending...', file=sys.stdout)
            print(r.text, file=sys.stdout)


    def send(self):
        """Start sending the message and attachments."""
        self.construct_message()
        self.send_content('/sendMessage')
        for a in self.attachments:
            self.message['document'] = a
            self.send_content(method='/sendDocument')


    def send_async(self):
        """Send message asynchronously."""
        MESSAGELOOP.add_message(self)
