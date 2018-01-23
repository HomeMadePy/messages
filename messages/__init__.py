"""
messages - A package designed to make sending various types of messages easy.
"""

from .email_ import Email
from .slack import SlackWebHook
from .text import Twilio


__version__ = '0.1.0'
