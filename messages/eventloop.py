"""
Module that will handle asynchronous message sending, so each message will
be non-blocking.
"""

from collections import deque

import gevent
from gevent import monkey

monkey.patch_all()


class MessageLoop:
    """Asynchronous message sending loop."""

    def __init__(self):
        self.messages = deque()


    def add_message(self, message):
        """add a message to the event loop."""
        self.messages.append(message)
        self.send_loop()


    def send_loop(self):
        """start event loop."""
        #self.loop = asyncio.get_event_loop()
        tasks = []
        while self.messages:
            msg = self.messages.popleft()
            if hasattr(msg, 'send'):
                tasks.append(gevent.spawn(msg.send))


MESSAGELOOP = MessageLoop()
