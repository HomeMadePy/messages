"""messages.whatsapp tests."""

import pytest
import requests

import messages.whatsapp
from messages.whatsapp import WhatsApp
from messages.whatsapp import check_config_file
from messages._eventloop import MESSAGELOOP


##############################################################################
# FIXTURES
##############################################################################

@pytest.fixture()
def get_whap(mocker):
    """Return a valid WhatsApp instance."""
    configure_mock = mocker.patch.object(messages.whatsapp, 'check_config_file')
    return WhatsApp(from_='+16198675309', to='+16195551212',
            auth=('test_sid', 'test_token'), body='test text!',
            attachments='https://imgs.xkcd.com/comics/python.png',
            profile='tester', save=False)


##############################################################################
# TESTS: WhatsApp.__init__
##############################################################################

def test_whatsapp_init(get_whap, cfg_mock):
    """
    GIVEN a need to create an WhatsApp object
    WHEN the user instantiates a new object with required args
    THEN assert WhatsApp object is created with given args
    """
    w = get_whap
    assert w.from_ == 'whatsapp:+16198675309'
    assert w.to == 'whatsapp:+16195551212'
    assert w.auth == '***obfuscated***'
    assert '_auth' in w.__dict__
    assert w._auth == ('test_sid', 'test_token')
    assert w.body == 'test text!'
    assert w.attachments == 'https://imgs.xkcd.com/comics/python.png'
