"""
messages - A package designed to make sending various types of messages easy.
"""

from .api import send
from .email_ import Email
from .slack import SlackWebhook
from .text import Twilio


MESSAGES = ('email', 'slackwebhook', 'twilio')

__version__ = '0.1.2'
