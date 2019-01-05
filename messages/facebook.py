"""
Module designed to make creating and sending chat messages easy.

1.  Facebook
    - Send messages via fbchat api
    - https://fbchat.readthedocs.io/en/master/index.html
"""

import reprlib

from fbchat import Client
import fbchat.models as fbchat_models

from ._config import check_config_file
from ._eventloop import MESSAGELOOP
from ._interface import Message
from ._utils import credential_property
from ._utils import validate_property
from ._utils import timestamp


class Facebook(Message):
    """
    Create and send text SMS/MMS text messages using the Twilio API.

    Args:
        :from_: (str) Email address that is used to log into Facebook.
        :to: (str) For group messages: You only need to navigate to
            https://www.facebook.com/messages/, click on the group you want to find the
            ID of, and then read the id from the address bar. The URL will look
            something like this: https://www.facebook.com/messages/t/1234567890, where
            1234567890 would be the ID of the group.
            - For users it is similar but the easiest way is to use a site like
            https://findmyfbid.in/ : The manual way is similar to group messages,
            however, sometimes the URL is firstname.lastname.number (e.g. john.doe.8)
            after /t/ instead of a random string of numbers. In this case there is a
            number of ways to get the ID. The a simple way to find their ID is to
            right click their name from https://www.facebook.com/messages/ then click
            "Copy Link Address". You can paste this in and get their ID which is the
            random string of numbers after https://www.facebook.com/messages/t/
        :auth: (str) Password for Facebook account.
        :body: (str) Message to send. It defaults to "(Y)" since that sends a thumbsup
            emoji and facebook does not allow you to send blank messages
        :attachments: (str) file to attach
            i.e. '/home/you/file2.pdf' or 'https://www.example.com/coolpicture.jpg'
        :profile: (str) use a separate account profile specified by name
        :save: (bool) save pertinent values in the messages config file,
            such as from_, to, thread_type, auth_token (encrypted keyring) to make
            sending messages faster.

    Attributes:
        :message_id: (str) return value from send, record of sent message

    Managed Attributes (Properties):
        :auth: auth will set as a private attribute (_auth) and obscured when requested
        :from_: user input will validate a proper email address
        :to: user input will validate a proper integer as a string
        :local_attachment: user input will be validated for a proper file path
        :remote_attachment: user input will be validated for a proper url

    Usage:
        Create a Facebook object with required Args above.
        Send message with self.send() or self.send_async() methods.

    Notes:
        For API description:
        https://fbchat.readthedocs.io/en/master/intro.html
    """

    auth = credential_property("auth")
    to = validate_property("to")
    local_attachment = validate_property("local_attachment")
    remote_attachment = validate_property("remote_attachment")

    def __init__(
        self,
        from_=None,
        auth=None,
        to=None,
        thread_type=None,
        body="",
        local_attachment=None,
        remote_attachment=None,
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
        self.local_attachment = local_attachment or []
        self.remote_attachment = remote_attachment or []
        self.logout = logout
        self.save = save
        self.verbose = verbose
        self.profile = profile
        self.message_id = None

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
            "{}Local Attachments: {}"
            "{}Remote Attachments: {}"
            "{}Message ID: {}".format(
                indentation,
                self.from_,
                indentation,
                self.to,
                indentation,
                self.thread_type,
                indentation,
                reprlib.repr(self.body),
                indentation,
                self.local_attachment,
                indentation,
                self.remote_attachment,
                indentation,
                self.message_id,
            )
        )

    def _add_body(self):
        """Add body, (Y) - which is a thumbs up, if no attachments"""
        if self.local_attachment or self.remote_attachment:
            self.body = self.body
        else:
            if self.body is '':
                self.body = "(Y)"

    def send(self):
        """Compose and start sending the message."""
        if self.verbose:
            print(
                "Debugging info"
                "\n--------------"
                "\n{} Message created.".format(timestamp())
            )

        self._add_body()

        client = Client(self.from_, self._auth)

        if self.thread_type not in ['USER', 'GROUP']:
            raise ValueError("Thread type must be either USER or GROUP.")
        else:
            if self.thread_type == "USER":
                if self.local_attachment or self.remote_attachment:
                    self.message_id = client.sendLocalFiles(
                        self.local_attachment,
                        message=self.body,
                        thread_id=self.to,
                        thread_type=fbchat_models.ThreadType.USER,
                    )
                    self.message_id = client.sendRemoteFiles(
                        self.remote_attachment,
                        thread_id=self.to,
                        thread_type=fbchat_models.ThreadType.USER,
                    )
                else:
                    print(self.body)
                    self.message_id = client.send(
                        fbchat_models.Message(text=self.body),
                        thread_id=self.to,
                        thread_type=fbchat_models.ThreadType.USER,
                    )
            elif self.thread_type == "GROUP":
                if self.local_attachment or self.remote_attachment:
                    self.message_id = client.sendLocalFiles(
                        self.local_attachment,
                        message=self.body,
                        thread_id=self.to,
                        thread_type=fbchat_models.ThreadType.GROUP,
                    )
                    self.message_id = client.sendRemoteFiles(
                        self.remote_attachment,
                        thread_id=self.to,
                        thread_type=fbchat_models.ThreadType.GROUP,
                    )
                else:
                    self.message_id = client.send(
                        fbchat_models.Message(text=self.body),
                        thread_id=self.to,
                        thread_type=fbchat_models.ThreadType.GROUP,
                    )

        if self.logout:
            print("Successfully logged out.")
            client.logout()

        if self.verbose:
            print(
                timestamp(),
                type(self).__name__ + " info:",
                self.__str__(indentation="\n * "),
            )

        print("Message sent.")

    def send_async(self):
        """Send message asynchronously."""
        MESSAGELOOP.add_message(self)
