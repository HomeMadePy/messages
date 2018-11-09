"""
Module that will handle asynchronous message sending, so each message will
be non-blocking.
"""

import asyncio

from ._exceptions import UnsupportedMessageTypeError


class MessageLoop:
    """Asynchronous message sending loop."""

    def __init__(self):
        self.loop = asyncio.get_event_loop()

    def add_message(self, message):
        """Add a message to the event loop."""
        try:
            self.send_loop(message)
        except AttributeError:
            raise UnsupportedMessageTypeError(message.__class__.__name__)

    def send_loop(self, msg, executor=None):
        """Send the message via the event loop."""
        self.loop.run_in_executor(executor, msg.send)


MESSAGELOOP = MessageLoop()
