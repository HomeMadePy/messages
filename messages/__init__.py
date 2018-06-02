"""
messages - A package designed to make sending various types of messages easy.
"""

from .api import send
from .email_ import Email
from .slack import SlackWebhook
from .telegram import TelegramBot
from .text import Twilio


__version__ = '0.4.0'


MESSAGES = {
    'email': {
        'defaults': ['from_', 'server', 'port',],
        'credentials': ['password']
    },
    'slackwebhook': {
        'defaults': ['from_', 'url'],
        'credentials': []
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
