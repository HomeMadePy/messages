"""
Module designed to make creating and sending text messages easy.

1.  Twilio
    - Uses the Twilio API to send text messages.
    - Must have an account_sid, auth_token, and a twilio phone number
      in order to use.
    - Go to https://www.twilio.com to register.
"""

import sys
from collections import deque

from twilio.rest import Client

from .config import configure
from ._eventloop import MESSAGELOOP
from ._interface import Message


class Twilio(Message):
    """
    Create and send text SMS/MMS text messages using the Twilio API.

    Args:
        :from_: (str) phone number of originating text, e.g. '+15558675309'
        :to: (str) phone number of destination text, e.g. '+15558675309'
        :acct_sid: (str) api credential from twilio
        :auth_token: (str) api credential from twilio
        :body: (str) message to send
        :attachments: (str) url of any image to send along with message
        :profile: (str) use a separate account profile specified by name
        :save: (bool) save pertinent values in the messages config file,
            such as from_, acct_sid, auth_token (encrypted keyring) to make
            sending messages faster.

    Attributes:
        :client: (Client) twilio.rest client for authentication
        :sid: (str) return value from send, record of sent message

    Usage:
        Create a text message (SMS/MMS) object with required Args above.
        Send text message with self.send() or self.send_async() methods.

    Notes:
        For API description:
        https://www.twilio.com/docs/api/messaging/send-messages
    """

    def __init__(
        self, from_=None, to=None, acct_sid=None, auth_token=None,
        body='', attachments=None, profile=None, save=False
    ):

        config_kwargs = {'from_': from_, 'acct_sid': acct_sid,
                'auth_token': auth_token, 'profile': profile, 'save': save}

        configure(self, params=config_kwargs,
                to_save={'from_', 'acct_sid'}, credentials={'auth_token'})

        self.to = to
        self.body = body
        self.attachments = attachments
        self.client = None
        self.sid = None
        self.sent_messages = deque()


    def __str__(self):
        """print(Twilio(**args)) method."""
        return('Twilio Text Message:'
               '\n\tFrom: {}'
               '\n\tTo: {}'
               '\n\tbody: {}...'
               '\n\tattachments: {}'
               .format(self.from_, self.to, self.body, self.attachments))


    def get_client(self):
        """Return a twilio.rest client."""
        return Client(self.acct_sid, self.auth_token)

    def send(self):
        """
        Send the SMS/MMS message.
        Set self.sid to return code of message.
        Append the (sid, message) tuple to self.sent_messages as a history.
        """
        if self.client is None:
            self.client = self.get_client()
        msg = self.client.messages.create(
              to=self.to,
              from_=self.from_,
              body=self.body,
              media_url=self.attachments,
            )
        self.sid = msg.sid
        print('Message sent...', file=sys.stdout)
        self.sent_messages.append((msg.sid, repr(self)))


    def send_async(self):
        """Send message asynchronously."""
        MESSAGELOOP.add_message(self)
