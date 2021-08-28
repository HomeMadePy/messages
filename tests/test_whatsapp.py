"""messages.whatsapp tests."""

import pytest
import requests

import messages.whatsapp
from messages.whatsapp import WhatsApp


##############################################################################
# FIXTURES
##############################################################################

@pytest.fixture()
def get_whap():
    """Return a valid WhatsApp instance."""
    return WhatsApp(from_='+16198675309', to='+16195551212',
            auth=('test_sid', 'test_token'), body='test text!',
            attachments='https://imgs.xkcd.com/comics/python.png')


##############################################################################
# TESTS: WhatsApp.__init__
##############################################################################

def test_whatsapp_init(get_whap):
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
