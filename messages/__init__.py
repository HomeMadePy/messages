"""
messages - A package designed to make sending various types of messages easy.
"""

import logging

from .email_ import Email
from .slack import SlackWebhook
from .slack import SlackPost
from .telegram import TelegramBot
from .text import Twilio
from .whatsapp import WhatsApp

from ._exceptions import MessageSendError


__version__ = "0.8.0"


# Setup logger
logging.getLogger(__name__).addHandler(logging.NullHandler())
