"""
Module designed to make creating and sending text messages easy.

1.  Twilio
    - Uses the Twilio API to send text messages.
    - Must have an account_sid, auth_token, and a twilio phone number
      in order to use.
    - Go to https://www.twilio.com to register.
"""

import sys

import requests

from ._config import configure
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
        body='', attachments=None, profile=None, save=False, verbose=False
    ):

        config_kwargs = {'from_': from_, 'acct_sid': acct_sid,
                'auth_token': auth_token, 'profile': profile, 'save': save}

        configure(self, params=config_kwargs,
                to_save={'from_', 'acct_sid'}, credentials={'auth_token'})

        self.to = to
        self.body = body
        self.attachments = attachments
        self.sid = None
        self.verbose = verbose


    def __str__(self, indentation='\n'):
        """print(Email(**args)) method.
           Indentation value can be overridden in the function call.
           The default is new line"""
        return('{}From: {}'
               '{}To: {}'
               '{}Body: {}...'
               '{}Attachments: {}'
               '{}SID: {}'
               .format(indentation, self.from_,
                       indentation, self.to,
                       indentation, self.body[0:40],
                       indentation, self.attachments,
                       indentation, self.sid))


    def send(self):
        """
        Send the SMS/MMS message.
        Set self.sid to return code of message.
        """
        from ._utils import timestamp

        url = ('https://api.twilio.com/2010-04-01/Accounts/'
               + self.acct_sid + '/Messages.json')
        data = {
            'From': self.from_,
            'To': self.to,
            'Body': self.body,
            'MediaUrl': self.attachments,
        }

        if self.verbose:
            print('Debugging info'
                  '\n--------------'
                  '\n{} Message created.'.format(timestamp()))

        r = requests.post(url, data=data, auth=(self.acct_sid, self.auth_token))
        self.sid = r.json()['sid']

        if self.verbose:
            print(timestamp(), type(self).__name__ + ' info:',
                self.__str__(indentation='\n * '))

        print('Message sent.')


    def send_async(self):
        """Send message asynchronously."""
        MESSAGELOOP.add_message(self)
