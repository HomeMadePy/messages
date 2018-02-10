"""This module implements the Messages API."""

import copy
import inspect

from .email_ import Email
from .slack import SlackWebhook
from .text import Twilio


MSG = {'email': {'args': {arg:None for arg in inspect.getargspec(Email).args
                                   if arg!='self'},
                 'class': Email},
       'slackwebhook': {'args': {arg:None for arg in inspect.getargspec(SlackWebhook).args
                                          if arg!='self'},
                        'class': SlackWebhook},
       'twilio': {'args': {arg:None for arg in inspect.getargspec(Twilio).args
                                    if arg!='self'},
                  'class': Twilio},
            }


def send(msg_type, send_async=False, **kwargs):
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
                      server_name: 'smtp.google.com',
                      server_port: 465,
                      password: 'yourPassword',
                      from_: 'me@here.com',
                      to: 'you@there.com',
                      cc: None,
                      bcc: None,
                      subject: 'Email Subject',
                      body: 'Your message to send',
                      attachments: ['filepath1', 'filepath2'],
                }
        >>> messages.send('email', **kwargs)
        Message sent...
    """
    message = message_factory(msg_type, **kwargs)

    if send_async:
        message.send_async()
    else:
        message.send()


def message_factory(msg_type, **kwargs):
    """Factory function to return the specified message instance."""
    args = copy.copy(MSG[msg_type.lower()]['args'])
    args.update(kwargs)
    return MSG[msg_type.lower()]['class'](**args)
