"""integration tests for messages.telegram module."""

import pytest
import int_setup

from messages.telegram import TelegramBot
from messages._exceptions import MessageSendError

##############################################################################
# SKIP TESTS IF ENVIRONMENT NOT PREPPED
##############################################################################

#Skip all tests if not configured
pytestmark = pytest.mark.skipif(not int_setup.integration_test_configured('telegrambot'),
    reason='Tester not configured for messages.telegram.TelegramBot')


#############################################################################
# FIXTURES
##############################################################################

@pytest.fixture()
def get_tgram():
    return TelegramBot(
            profile='integration_tester',
            from_='Integration Tester',
            subject='[Messages] Integration Testing',
            body='Conducting Integration Testing',
            attachments='https://imgs.xkcd.com/comics/python.png',
            save=False,
        )

##############################################################################
# TESTS: TelegramBot.send()
##############################################################################

def test_tgram_send_good(get_tgram):
    """
    GIVEN a message to send on Telegram
    WHEN send() is called
    THEN assert message is sent with no errors
    """
    t = get_tgram
    t.send()


def test_tgram_send_raisesExc(get_tgram):
    """
    GIVEN a message to send on Telegram
    WHEN send() is called but with a bad auth credential
    THEN assert MessageSendError is raised
    """
    t = get_tgram
    t._auth = 'BadCred'
    t.base_url = "https://api.telegram.org/bot" + t._auth
    with pytest.raises(MessageSendError):
        t.send()
