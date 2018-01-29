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

import attr
from attr.validators import instance_of
from twilio.rest import Client

from .eventloop import MESSAGELOOP
from ._interface import Message


@attr.s
class Twilio(Message):
    """
    Create and send text SMS/MMS text messages using the Twilio API.

    Args:
        :acct_sid: str, api credential from twilio
        :auth_token: str, api credential from twilio\
        :from_: str, phone number of originating text, e.g. '+15558675309'
        :to: str, phone number of destination text, e.g. '+15558675309'
        :body: str, message to send
        :media_url: str, url of any image to send along with message

    Attributes:
        :client: Client, twilio.rest client for authentication
        :sid: str, return value from send, record of sent message

    Usage:
        Create a text message (SMS/MMS) object with required Args above.
        Send text message with self.send() or self.send_async() methods.

    Notes:
        For API description:
        https://www.twilio.com/docs/api/messaging/send-messages
    """

    acct_sid = attr.ib(validator=instance_of(str))
    auth_token = attr.ib(validator=instance_of(str))
    from_ = attr.ib(validator=instance_of(str))
    to = attr.ib(validator=instance_of(str))
    body = attr.ib()
    media_url = attr.ib()
    client = Client(acct_sid, auth_token)
    sid = None
    sent_messages = deque()


    def __str__(self):
        """print(Twilio(**args)) method."""
        return('Twilio Text Message:'
               '\n\tFrom: {}'
               '\n\tTo: {}'
               '\n\tbody: {}...'
               '\n\tmedia_url: {}'
               .format(self.from_, self.to, self.body, self.media_url))


    def send(self):
        """
        Send the SMS/MMS message.
        Set self.sid to return code of message.
        Append the (sid, message) tuple to self.sent_messages as a history.
        """
        msg = self.client.messages.create(
              to = self.to,
              from_ = self.from_,
              body = self.body,
              media_url = self.media_url,
            )
        self.sid = msg.sid
        print('Message sent...', file=sys.stdout)
        self.sent_messages.append((msg.sid, repr(self)))


    def send_async(self):
        """Send message asynchronously."""
        MESSAGELOOP.add_message(self)
