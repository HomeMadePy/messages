"""
Module designed to make creating and sending text messages easy.

1.  Twilio
    - Uses the Twilio API to send text messages.
    - Must have an account_sid, auth_token, and a twilio phone number
      in order to use.
    - Go to https://www.twilio.com to register.
"""

import reprlib

import httpx

from ._exceptions import MessageSendError
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

    Attributes:
        :sid: (str) return value from send, record of sent message

    Managed Attributes (Properties):
        :auth: auth will set as a private attribute (_auth) and obscured when requested
        :from_: user input will be validated for a proper phone number
        :to: user input will be validated for a proper phone number
        :attachments: user input will be validated for a proper url

    Usage:
        Create a text message (SMS/MMS) object with required Args above.
        Send text message with self.send() self.send_async() methods.

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
        verbose=False,
    ):

        self.from_ = from_
        self.to = to
        self.auth = auth
        self.body = body
        self.attachments = attachments
        self.verbose = verbose
        self.sid = None

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

    def _construct_message(self):
        """Format message params."""
        self.url = (
            "https://api.twilio.com/2010-04-01/Accounts/"
            + self._auth[0]
            + "/Messages.json"
        )
        self.data = {
            "From": self.from_,
            "To": self.to,
            "Body": self.body,
        }

        if self.attachments:
            self.data.update({"MediaUrl": self.attachments,})

        if self.verbose:
            print(
                "Debugging info"
                "\n--------------"
                "\n{} Message created.".format(timestamp())
            )

    def send(self):
        """
        Send the SMS/MMS message synchronously.
        Set self.sid to return code of message.
        """
        self._construct_message()
        try:
            resp = httpx.post(self.url, data=self.data, auth=(self._auth[0], self._auth[1]))
            resp.raise_for_status()
        except httpx.HTTPStatusError as e:
            exc = "{}".format(e)
            raise MessageSendError(exc)

        self.sid = resp.json()["sid"]

        if self.verbose:
            print(
                timestamp(),
                type(self).__name__ + " info:",
                self.__str__(indentation="\n * "),
                "\n * HTTP status code:",
                resp.status_code,
            )

        print("Message sent.")

        return resp


    async def send_async(self):
        """
        Send the SMS/MMS message asynchronously.
        Set self.sid to return code of message.
        """
        self._construct_message()
        try:
            async with httpx.AsyncClient(timeout=None) as client:
                resp = await client.post(self.url, data=self.data, auth=(self._auth[0], self._auth[1]))
            resp.raise_for_status()
        except httpx.HTTPStatusError as e:
            exc = "{}".format(e)
            raise MessageSendError(exc)

        self.sid = resp.json()["sid"]
        return resp
