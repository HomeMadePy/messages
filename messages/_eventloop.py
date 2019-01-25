"""
Module that will handle asynchronous message sending, so each message will
be non-blocking.
"""

from concurrent.futures.thread import ThreadPoolExecutor as PoolExecutor

from ._exceptions import UnsupportedMessageTypeError


def _send_coroutine():
    """
    Creates a running coroutine to receive message instances and send
    them in a futures executor.
    """
    with PoolExecutor() as executor:
        while True:
            msg = yield
            future = executor.submit(msg.send)
            future.add_done_callback(_exception_handler)


def _exception_handler(future):
    """Catch exceptions from pool executor and reraise in main thread."""
    exc = future.exception()
    if exc:
        raise exc


class MessageLoop:
    """Asynchronous message sending loop."""

    def __init__(self):
        self._coro = _send_coroutine()
        next(self._coro)

    def add_message(self, msg):
        """Add a message to the futures executor."""
        try:
            self._coro.send(msg)
        except AttributeError:
            raise UnsupportedMessageTypeError(msg.__class__.__name__)


MESSAGELOOP = MessageLoop()
