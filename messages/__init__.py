"""
messages - A package designed to make sending various types of messages easy.
"""

import logging

from .api import send

from .email_ import Email
from .slack import SlackWebhook
from .slack import SlackPost
from .telegram import TelegramBot
from .text import Twilio


__version__ = '0.4.3'


# Setup logger
logging.getLogger(__name__).addHandler(logging.NullHandler())


# dict values for cli module
MESSAGES = {
    'email': {
        'defaults': ['from_', 'server', 'port',],
        'credentials': ['auth']
    },
    'slackwebhook': {
        'defaults': ['from_'],
        'credentials': ['auth']
    },
    'slackpost': {
        'defaults': ['channel'],
        'credentials': ['auth']
    },
    'telegrambot': {
        'defaults': ['from_', 'chat_id'],
        'credentials': ['auth']
    },
    'twilio': {
        'defaults': ['from_'],
        'credentials': ['acct_sid', 'auth_token']
    },
}
