"""
Module designed to make creating and sending chat messages easy.

1.  Slack
    - This is a base class that has the useful API for the other slack
      messages.
    - This is not to be instantiated on its own.

2.  SlackWebhook
    - Send messages via the Incoming Webhooks feature
    - https://api.slack.com/incoming-webhooks
    - Inherits functionality/API from the Slack class

3.  SlackPost
    - Send messages via the Slack chat.postMessage API
    - https://api.slack.com/methods/chat.postMessage
    - Inherits functionality/API from the Slack class
"""

import reprlib

import requests

from ._config import check_config_file
from ._eventloop import MESSAGELOOP
from ._interface import Message
from ._utils import credential_property
from ._utils import validate_property
from ._utils import timestamp


class Slack(Message):
    """Base class that Slack* classes inherit from."""

    def _construct_message(self):
        """Build the message params."""
        self.message["text"] = ""
        if self.from_:
            self.message["text"] += "From: " + self.from_ + "\n"
        if self.subject:
            self.message["text"] += "Subject: " + self.subject + "\n"

        self.message["text"] += self.body
        self._add_attachments()

    def _add_attachments(self):
        """Add attachments."""
        if self.attachments:
            if not isinstance(self.attachments, list):
                self.attachments = [self.attachments]

            self.message["attachments"] = [
                {"image_url": url, "author_name": ""} for url in self.attachments
            ]
            if self.params:
                for attachment in self.message["attachments"]:
                    attachment.update(self.params)

    def send(self, encoding="json"):
        """Send the message via HTTP POST, default is json-encoded."""
        self._construct_message()
        if self.verbose:
            print(
                "Debugging info"
                "\n--------------"
                "\n{} Message created.".format(timestamp())
            )

        if encoding == "json":
            resp = requests.post(self.url, json=self.message)
        elif encoding == "url":
            resp = requests.post(self.url, data=self.message)

        if self.verbose:
            print(
                timestamp(),
                type(self).__name__,
                " info:",
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


class SlackWebhook(Slack):
    """
    Create and send Slack message via the Incoming WebHooks API.

    Args:
        :from_: (str) optional arg to specify who message is from.
        :auth: (str) webhook url for installed slack app.
        :subject: (str) optional arg to specify message subject.
        :body: (str) message to send.
        :attachments: (str or list) each item is a url to attach
        :params: (dict) additional attributes to add to each attachment,
            i.e. author_name, title, text, etc., see API for information
            on which attributes are possible.
        :profile: (str) use a separate account profile specified by name
        :save: (bool) save pertinent values in the messages config file,
            such as from_, url (encrypted keyring) to make
            sending messages faster.

    Attributes:
        :message: (dict) current form of the message to be constructed

    Managed Attributes (Properties):
        :auth: auth will set as a private attribute (_auth) and obscured when requested
        :attachments: user input will be validated for a proper url

    Usage:
        Create a SlackWebhook object with required Args above.
        Send message with self.send() or self.send_async() methods.

    Note:
        For API description:
        https://api.slack.com/incoming-webhooks
    """

    auth = credential_property("auth")
    attachments = validate_property("attachments")

    def __init__(
        self,
        from_=None,
        auth=None,
        subject=None,
        body="",
        attachments=None,
        params=None,
        profile=None,
        save=False,
        verbose=False,
    ):

        self.from_ = from_
        self.auth = auth
        self.subject = subject
        self.body = body
        self.attachments = attachments or []
        self.params = params
        self.profile = profile
        self.save = save
        self.verbose = verbose
        self.message = {}

        if self.profile:
            check_config_file(self)

        self.url = self._auth

    def __str__(self, indentation="\n"):
        """print(SlackWebhook(**args)) method.
           Indentation value can be overridden in the function call.
           The default is new line"""
        return (
            "{}URL: {}"
            "{}From: {}"
            "{}Subject: {}"
            "{}Body: {}"
            "{}Attachments: {}".format(
                indentation,
                self.url,
                indentation,
                self.from_ or "Not Specified",
                indentation,
                self.subject,
                indentation,
                reprlib.repr(self.body),
                indentation,
                self.attachments,
            )
        )


class SlackPost(Slack):
    """
    Create and send Slack message via the Slack chat.poseMessage API

    Args:
        :from_: (str) optional arg to specify who message is from.
        :auth: (str) authentication token with required scopes.
        :channel: (str) Channel, private group, or IM channel to send message
        :subject: (str) optional arg to specify message subject.
        :body: (str) message to send.
        :attachments: (str or list) each item is a url to attach
        :params: (dict) additional attributes to add to each attachment,
            i.e. author_name, title, text, etc., see API for information
            on which attributes are possible.
        :profile: (str) use a separate account profile specified by name
        :save: (bool) save pertinent values in the messages config file,
            such as from_, url (encrypted keyring) to make
            sending messages faster.

    Attributes:
        :message: (dict) current form of the message to be constructed

    Managed Attributes (Properties):
        :auth: auth will set as a private attribute (_auth) and obscured when requested
        :attachments: user input will be validated for a proper url
        :channel: user input will be validated for a proper string

    Usage:
        Create a SlackPost object with required Args above.
        Send message with self.send() or self.send_async() methods.

    Note:
        For API description:
        https://api.slack.com/methods/chat.postMessage
    """

    auth = credential_property("auth")
    attachments = validate_property("attachments")
    channel = validate_property("channel")

    def __init__(
        self,
        from_=None,
        auth=None,
        channel=None,
        subject=None,
        body="",
        attachments=None,
        params=None,
        profile=None,
        save=False,
        verbose=False,
    ):

        self.from_ = from_
        self.auth = auth
        self.channel = channel
        self.subject = subject
        self.body = body
        self.attachments = attachments or []
        self.params = params
        self.profile = profile
        self.save = save
        self.verbose = verbose
        self.url = "https://slack.com/api/chat.postMessage"

        if self.profile:
            check_config_file(self)

        self.message = {"token": self._auth, "channel": self.channel}

    def __str__(self, indentation="\n"):
        """print(SlackPost(**args)) method.
           Indentation value can be overridden in the function call.
           The default is new line"""
        return (
            "{}Channel: {}"
            "{}From: {}"
            "{}Subject: {}"
            "{}Body: {}"
            "{}Attachments: {}".format(
                indentation,
                self.channel,
                indentation,
                self.from_ or "Not Specified",
                indentation,
                self.subject,
                indentation,
                reprlib.repr(self.body),
                indentation,
                self.attachments,
            )
        )

    def send(self):
        """Send the message via HTTP POST, url-encoded."""
        super().send(encoding="url")
