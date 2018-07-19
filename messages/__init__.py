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


__version__ = '0.4.2'


# Setup logger
logging.getLogger(__name__).addHandler(logging.NullHandler())


# dict values for cli module
MESSAGES = {
    'email': {
        'defaults': ['from_', 'server', 'port',],
        'credentials': ['password']
    },
    'slackwebhook': {
        'defaults': ['from_', 'url'],
        'credentials': []
    },
    'slackpost': {
        'defaults': ['channel'],
        'credentials': ['token']
    },
    'telegrambot': {
        'defaults': ['from_', 'chat_id'],
        'credentials': ['bot_token']
    },
    'twilio': {
        'defaults': ['from_', 'acct_sid'],
        'credentials': ['auth_token']
    },
}
