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
