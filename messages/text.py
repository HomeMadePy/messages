"""
Module designed to make creating and sending text messages easy.

1. Twilio classes uses the Twilio API to send text messages.
   * Must have an account_sid, auth_token, and a twilio phone number
     in order to use.  Go to https://www.twilio.com to register.
"""

import sys

from collections import deque

from twilio.rest import Client


class Twilio:
    """
    Create and send text SMS/MMS text messages using the Twilio API.

    Args:
        acct_sid: str, api credential from twilio
        auth_token: str, api credential from twilio\
        from_: str, phone number of originating text, e.g. '+15558675309'
        to: str, phone number of destination text, e.g. '+15558675309'
        body: str, message to send
        media_url: str, url of any image to send along with message

    Usage:
        Create a text message (SMS/MMS) object with required Args above.
        Send text message with self.send() method.

    Notes:
        For API description:
        https://www.twilio.com/docs/api/messaging/send-messages
    """

    def __init__(self, acct_sid, auth_token, from_, to, body, media_url):
        self.acct_sid = acct_sid
        self.auth_token = auth_token
        self.client = Client(self.acct_sid, self.auth_token) #verify creds here and raise exception if bad
        self.from_ = from_
        self.to = to
        self.body = body
        self.media_url = None or media_url
        self.sid = None
        self.sent_texts = deque()


    def __str__(self):
        """print(Twilio(**args)) method."""
        return('Twilio Text Message:'
              '\n\tFrom: {}'
              '\n\tTo: {}'
              '\n\tbody: {}...'
              '\n\tmedia_url: {}'
              .format(self.from_, self.to, self.body, self.media_url))


    def __repr__(self):
        """repr(Twilio(**args)) method."""
        return('{}({}, {}, {}, {}, {}, {})'
               .format(self.__class__.__name__, self.acct_sid,
                       self.auth_token, self.from_, self.to,
                       self.body, self.media_url))


    def send(self):
        """
        Send the SMS/MMS message.
        Set self.sid to return code of message.
        Append the (sid, message) tuple to self.sent_texts
        """
        msg = self.client.messages.create(
            to = self.to,
            from_ = self.from_,
            body = self.body,
            media_url = self.media_url,
            )
        self.sid = msg.sid
        print('Message sent...', file=sys.stdout)
        self.sent_texts.append((msg.sid, repr(self)))
