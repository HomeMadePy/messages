"""
Module designed to make creating and sending text messages easy.

1.  Twilio
    - Uses the Twilio API to send text messages.
    - Must have an account_sid, auth_token, and a twilio phone number
      in order to use.
    - Go to https://www.twilio.com to register.
"""

import reprlib

import requests

from ._config import check_config_file
from ._eventloop import MESSAGELOOP
from ._interface import Message
from ._utils import credential_property
from ._utils import validate_property
from ._utils import timestamp


class Twilio(Message):
    """
    Create and send text SMS/MMS text messages using the Twilio API.

    Args:
        :from_: (str) phone number of originating text, e.g. '+15558675309'
        :to: (str) phone number of destination text, e.g. '+15558675309'
        :auth: (list or tuple) twilio api credentials: (acct_sid, auth_token)
        :body: (str) message to send.  Defaults to body=" " (one space) since
            Twilio doesn't allow an empty body to be sent
        :attachments: (str) url of any image to send along with message
        :profile: (str) use a separate account profile specified by name
        :save: (bool) save pertinent values in the messages config file,
            such as from_, acct_sid, auth_token (encrypted keyring) to make
            sending messages faster.

    Attributes:
        :sid: (str) return value from send, record of sent message

    Managed Attributes (Properties):
        :auth: auth will set as a private attribute (_auth) and obscured when requested
        :from_: user input will be validated for a proper phone number
        :to: user input will be validated for a proper phone number
        :attachments: user input will be validated for a proper url

    Usage:
        Create a text message (SMS/MMS) object with required Args above.
        Send text message with self.send() or self.send_async() methods.

    Notes:
        For API description:
        https://www.twilio.com/docs/api/messaging/send-messages
    """

    auth = credential_property("auth")
    from_ = validate_property("from_")
    to = validate_property("to")
    attachments = validate_property("attachments")

    def __init__(
        self,
        from_=None,
        to=None,
        auth=None,
        body=" ",
        attachments=None,
        profile=None,
        save=False,
        verbose=False,
    ):

        self.from_ = from_
        self.to = to
        self.auth = auth
        self.body = body
        self.attachments = attachments
        self.profile = profile
        self.save = save
        self.verbose = verbose
        self.sid = None

        if self.profile:
            check_config_file(self)

    def __str__(self, indentation="\n"):
        """print(Email(**args)) method.
           Indentation value can be overridden in the function call.
           The default is new line"""
        return (
            "{}From: {}"
            "{}To: {}"
            "{}Body: {}"
            "{}Attachments: {}"
            "{}SID: {}".format(
                indentation,
                self.from_,
                indentation,
                self.to,
                indentation,
                reprlib.repr(self.body),
                indentation,
                self.attachments,
                indentation,
                self.sid,
            )
        )

    def send(self):
        """
        Send the SMS/MMS message.
        Set self.sid to return code of message.
        """
        url = (
            "https://api.twilio.com/2010-04-01/Accounts/"
            + self._auth[0]
            + "/Messages.json"
        )
        data = {
            "From": self.from_,
            "To": self.to,
            "Body": self.body,
            "MediaUrl": self.attachments,
        }

        if self.verbose:
            print(
                "Debugging info"
                "\n--------------"
                "\n{} Message created.".format(timestamp())
            )

        resp = requests.post(url, data=data, auth=(self._auth[0], self._auth[1]))
        self.sid = resp.json()["sid"]

        if self.verbose:
            print(
                timestamp(),
                type(self).__name__ + " info:",
                self.__str__(indentation="\n * "),
                "\n * HTTP status code:",
                resp.status_code,
            )

        if resp.status_code >= 200 and resp.status_code < 300:
            print("Message sent.")
        else:
            print("Error while sending.  HTTP status code =", resp.status_code)

    def send_async(self):
        """Send message asynchronously."""
        MESSAGELOOP.add_message(self)
