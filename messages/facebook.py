"""
Module designed to make creating and sending chat messages easy.

1.  Facebook
    - Send messages via fbchat api
    - https://fbchat.readthedocs.io/en/master/index.html
"""

import reprlib

from fbchat import Client
import fbchat.models as fbchat_models
import requests

from ._config import check_config_file
from ._eventloop import MESSAGELOOP
from ._exceptions import MessageSendError
from ._interface import Message
from ._utils import credential_property
from ._utils import validate_property
from ._utils import timestamp


class Facebook(Message):
    """
    Create and send text SMS/MMS text messages using the Twilio API.

    Args:
        :from_: (str) Email address that is used to log into Facebook.
        :to: (str) For group messages: You only need to navigate to https://www.facebook.com/messages/,
            click on the group you want to find the ID of, and then read the id from the address bar.
            The URL will look something like this: https://www.facebook.com/messages/t/1234567890,
            where 1234567890 would be the ID of the group.
            - For users it is similar, however, sometimes the URL has like firstname.lastname.number
            (e.g. john.doe.8) after /t/ instead of a random string of numbers. This means your friend
            has customized her URL.In this case there is a number of ways to get the ID. The simplist
            way to find their ID is to right click their name from https://www.facebook.com/messages/
            then click "Copy Link Address". You can paste this in and get their ID which is the random
            string of numbers after https://www.facebook.com/messages/t/
            - More information here: https://fbchat.readthedocs.io/en/master/intro.html#threads
        :auth: (str) Password for Facebook account.
        :body: (str) Message to send. It defaults to "(Y)" since that sends a thumbsup emoji and facebook
            does not allow you to send blank messages
        :attachments: (str) not sure about these yet
            https://fbchat.readthedocs.io/en/master/api.html#fbchat.models.FileAttachment
        :profile: (str) use a separate account profile specified by name
        :save: (bool) save pertinent values in the messages config file,
            such as from_, to, thread_type, auth_token (encrypted keyring) to make
            sending messages faster.

    Attributes:
        :: STILL WORKING ON THIS

    Managed Attributes (Properties):
        :auth: auth will set as a private attribute (_auth) and obscured when requested
            - commented out right now since it won't log in with it
        :from_: user input will validate a proper email address

    Usage:
        Create a Facebook object with required Args above.
        Send message with self.send() or self.send_async() methods.

    Notes:
        For API description:
        https://fbchat.readthedocs.io/en/master/intro.html
    """

    auth = credential_property("auth")
    from_ = validate_property("from_")

    def __init__(
        self,
        from_=None,
        auth=None,
        to=None,
        thread_type=None,
        body="(Y)",
        logout=False,
        profile=None,
        save=False,
        verbose=False,
     ):

        self.from_ = from_
        self.auth = auth
        self.to = to  # thread_id
        self.thread_type = thread_type.upper()
        self.body = body
        self.logout = logout
        self.save = save
        self.verbose = verbose
        self.profile = profile

        if self.profile:
            check_config_file(self)

    def __str__(self, indentation="\n"):
        """print(Email(**args)) method.
           Indentation value can be overridden in the function call.
           The default is new line"""
        return (
            "{}From: {}"
            "{}To: {}"
            "{}Thread Type: {}"
            "{}Body: {}"
            "{}Message ID:".format(
                indentation,
                self.from_,
                indentation,
                self.to,
                indentation,
                self.thread_type,
                indentation,
                reprlib.repr(self.body),
                indentation,
            )
        )

    def send(self):
        """Compose and start sending the message."""
        if self.verbose:
            print(
                "Debugging info"
                "\n--------------"
                "\n{} Message created.".format(timestamp())
            )

        client = Client(self.from_, self._auth)

        if self.thread_type == "USER":
            try:
                message_id = client.send(fbchat_models.Message(text=self.body), thread_id=self.to, thread_type=fbchat_models.ThreadType.USER)
                client.logout()
            except requests.exceptions.HTTPError as e:
                raise MessageSendError(e)
        elif self.thread_type == "GROUP":
            try:
                message_id = client.send(fbchat_models.Message(text=self.body), thread_id=self.to, thread_type=fbchat_models.ThreadType.GROUP)
            except requests.exceptions.HTTPError as e:
                raise MessageSendError(e)
        else:
            raise ValueError("Thread type must be either USER or GROUP.")

        if self.logout:
            print("Successfully logged out.")
            client.logout()

        if self.verbose:
            print(
                timestamp(),
                type(self).__name__ + " info:",
                self.__str__(indentation="\n * "),
                message_id,
            )

        print("Message sent.")

    def send_async(self):
        """Send message asynchronously."""
        MESSAGELOOP.add_message(self)
