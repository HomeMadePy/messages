"""This module implements the Messages API."""

import sys

from .email_ import Email
from .facebook import Facebook
from .slack import SlackWebhook
from .slack import SlackPost
from .telegram import TelegramBot
from .text import Twilio
from .whatsapp import WhatsApp

from ._exceptions import InvalidMessageInputError
from ._exceptions import UnsupportedMessageTypeError
from ._exceptions import UnknownProfileError
from ._exceptions import MessageSendError


MESSAGE_CLASSES = {Email, Facebook, SlackWebhook, SlackPost, TelegramBot, Twilio, WhatsApp}
MESSAGE_TYPES = {i.__name__.lower(): i for i in MESSAGE_CLASSES}


def send(msg_type, send_async=False, *args, **kwargs):
    """
    Constructs a message class and sends the message.
    Defaults to sending synchronously.  Set send_async=True to send
    asynchronously.

    Args:
        :msg_type: (str) the type of message to send, i.e. 'Email'
        :send_async: (bool) default is False, set True to send asynchronously.
        :kwargs: (dict) keywords arguments that are required for the
            various message types.  See docstrings for each type.
            i.e. help(messages.Email), help(messages.Twilio), etc.

    Example:
        >>> kwargs = {
                  from_: 'me@here.com',
                  to: 'you@there.com',
                  auth: 'yourPassword',
                  subject: 'Email Subject',
                  body: 'Your message to send',
                  attachments: ['filepath1', 'filepath2'],
            }
        >>> messages.send('email', **kwargs)
        Message sent...
    """
    message = message_factory(msg_type, *args, **kwargs)

    try:
        if send_async:
            message.send_async()
        else:
            message.send()
    except MessageSendError as e:
        err_exit("Unable to send message: ", e)


def message_factory(msg_type, msg_types=MESSAGE_TYPES, *args, **kwargs):
    """
    Factory function to return the specified message instance.

    Args:
        :msg_type: (str) the type of message to send, i.e. 'Email'
        :msg_types: (str, list, or set) the supported message types
        :kwargs: (dict) keywords arguments that are required for the
            various message types.  See docstrings for each type.
            i.e. help(messages.Email), help(messages.Twilio), etc.
    """
    try:
        return msg_types[msg_type.lower()](*args, **kwargs)
    except (UnknownProfileError, InvalidMessageInputError) as e:
        err_exit("Unable to send message: ", e)
    except KeyError:
        raise UnsupportedMessageTypeError(msg_type, msg_types)


def err_exit(msg, err):
    """Utility function to print an error message, then call SystemExit."""
    print(msg, err)
    sys.exit(1)
