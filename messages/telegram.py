"""
Module designed to make creating and sending chat messages easy.

1.  TelegramBot
    - Send messages via the Telegram Bot feature
    - https://core.telegram.org/bots
"""

import reprlib

import httpx

from ._exceptions import MessageSendError
from ._interface import Message
from ._utils import credential_property
from ._utils import validate_property
from ._utils import timestamp


class TelegramBot(Message):
    """
    Create and send Telegram message via the Telegram Bot API.

    Args:
        :from_: (str) optional arg to specify who message is from.
        :to: (str) if chat_id is unknown, can specify username of
            recipient to lookup via API call.  This may return None if
            chat is older than 24-hours old.
        :auth: (str) auth token for bot for access.
        :chat_id: (str) chat_id for already-intiated chat.
            chat_id is an integer represented as a string.
            Recipient must have already initiated chat at some
            point in the past for bot to send message.
        :subject: (str) optional arg to specify message subject.
        :body: (str) message to send.
        :attachments: (str or list) each item is a url to attach
        :params: (dict) additional attributes to add to message,
            i.e. parse_mode (HTML or Markdown, see API for information
            on which attributes are possible.

    Attributes:
        :message: (dict) current form of the message to be constructed

    Managed Attributes (Properties):
        :auth: auth will set as a private attribute (_auth) and obscured when requested
        :chat_id: user input will validate a proper integer as a string

    Usage:
        Create a TelegramBot object with required Args above.
        Send message with self.send() or self.send_async() methods.

    Note:
        For API description:
        https://core.telegram.org/bots/api#available-methods
    """

    auth = credential_property("auth")
    chat_id = validate_property("chat_id")

    def __init__(
        self,
        from_=None,
        to=None,
        auth=None,
        chat_id=None,
        subject=None,
        body="",
        attachments=None,
        params=None,
        verbose=False,
    ):

        self.from_ = from_
        self.to = to
        self.auth = auth
        self.chat_id = chat_id
        self.subject = subject
        self.body = body
        self.attachments = attachments or []
        self.params = params or {}
        self.verbose = verbose
        self.message = {}
        self.base_url = "https://api.telegram.org/bot" + self._auth

    def __str__(self, indentation="\n"):
        """print(Telegram(**args)) method.
           Indentation value can be overridden in the function call.
           The default is new line"""
        return (
            "{}From: {}"
            "{}To: {}"
            "{}Chat ID: {}"
            "{}Subject: {}"
            "{}Body: {}"
            "{}Attachments: {}".format(
                indentation,
                self.from_,
                indentation,
                self.to,
                indentation,
                self.chat_id,
                indentation,
                self.subject,
                indentation,
                reprlib.repr(self.body),
                indentation,
                self.attachments,
            )
        )

    def get_chat_id(self, username):
        """Lookup chat_id of username if chat_id is unknown via API call."""
        if username is not None:
            chats = httpx.get(self.base_url + "/getUpdates").json()
            user = username.split("@")[-1]
            for chat in chats["result"]:
                if chat["message"]["from"]["username"] == user:
                    return chat["message"]["from"]["id"]

    def _construct_message(self):
        """Build the message params."""
        self.message["chat_id"] = self.chat_id
        self.message["text"] = ""
        if self.from_:
            self.message["text"] += "From: " + self.from_ + "\n"
        if self.subject:
            self.message["text"] += "Subject: " + self.subject + "\n"

        self.message["text"] += self.body
        self.message.update(self.params)

    def _send_content(self, method="/sendMessage"):
        """send synchronously via HTTP Post."""
        url = self.base_url + method

        try:
            resp = httpx.post(url, json=self.message)
            resp.raise_for_status()
        except httpx.HTTPStatusError as e:
            exc = "{}".format(e)
            raise MessageSendError(exc)

        if self.verbose:
            if method == "/sendDocument":
                content_type = "Attachment: " + self.message["document"]
            elif method == "/sendMessage":
                content_type = "Message body"
            print(timestamp(), content_type, "sent.")

    def send(self):
        """Start sending the message and attachments."""
        self._construct_message()

        if self.verbose:
            print(
                "Debugging info"
                "\n--------------"
                "\n{} Message created.".format(timestamp())
            )

        self._send_content("/sendMessage")

        if self.attachments:
            if isinstance(self.attachments, str):
                self.attachments = [self.attachments]
            for a in self.attachments:
                self.message["document"] = a
                self._send_content(method="/sendDocument")

        if self.verbose:
            print(
                timestamp(),
                type(self).__name__ + " info:",
                self.__str__(indentation="\n * "),
            )

        print("Message sent.")

    async def _send_content_async(self, method="/sendMessage"):
        """send asynchronously via HTTP Post."""
        url = self.base_url + method

        try:
            async with httpx.AsyncClient() as client:
                resp = await client.post(url, json=self.message)
            resp.raise_for_status()
        except httpx.HTTPStatusError as e:
            exc = "{}".format(e)
            raise MessageSendError(exc)

    async def send_async(self):
        """Start sending the message and attachments."""
        self._construct_message()

        await self._send_content_async("/sendMessage")

        if self.attachments:
            if isinstance(self.attachments, str):
                self.attachments = [self.attachments]
            for a in self.attachments:
                self.message["document"] = a
                await self._send_content_async(method="/sendDocument")
