"""integration tests for messages.text module."""

import pytest

from messages.whatsapp import WhatsApp
from messages._exceptions import MessageSendError

from conftest import skip_if_on_travisCI


##############################################################################
# FIXTURES
##############################################################################

@pytest.fixture()
def get_whatsapp():
    """Return a valid WhatsApp instance."""
    return WhatsApp(to='+14159999999',
               body='[Messages] integration test',
               attachments='https://imgs.xkcd.com/comics/python.png')


##############################################################################
# TESTS: Send from
##############################################################################

@skip_if_on_travisCI
def test_whatsapp_normal_execution(get_whatsapp):
    """
    GIVEN a valid whatsapp object
    WHEN sending text message from valid number to valid number
    THEN assert response contains correct values
    """
    t = get_whatsapp
    resp = t.send()


@skip_if_on_travisCI
def test_whatsapp_with_empty_body(get_whatsapp):
    """
    GIVEN a valid whatsapp object
    WHEN sending text with empty body
    THEN assert error message body is required
    """
    t = get_whatsapp
    t.body = ''
    t.attachments = None

    with pytest.raises(MessageSendError) as resp:
        t.send()

    response = str(resp.value)
    assert '400' in response


@skip_if_on_travisCI
def test_whatsapp_send_from_unavailable_number(get_whatsapp):
    """
    GIVEN a valid whatsapp object
    WHEN sending text from unavailable number
    THEN assert error "from" number is not valid inbound phone number
    """
    t = get_whatsapp
    t.from_ = '+15005550000'

    with pytest.raises(MessageSendError) as resp:
        t.send()

    response = str(resp.value)
    assert '400' in response


@skip_if_on_travisCI
def test_whatsapp_send_from_invalid_number(get_whatsapp):
    """
    GIVEN a valid whatsapp object
    WHEN sending text from invalid number
    THEN assert error "from" number is not valid phone number
    """
    t = get_whatsapp
    t.from_ = '+15005550001'

    with pytest.raises(MessageSendError) as resp:
        t.send()

    response = str(resp.value)
    assert '400' in response


@skip_if_on_travisCI
def test_whatsapp_send_from_another_invalid_number(get_whatsapp):
    """
    GIVEN a valid whatsapp object
    WHEN sending text from a not valid sms-capable inbound number
    THEN assert error "from" number is not valid inbound phone number
    """
    t = get_whatsapp
    t.__dict__['from_'] = '+123'

    with pytest.raises(MessageSendError) as resp:
        t.send()

    response = str(resp.value)
    assert '400' in response


@skip_if_on_travisCI
def test_whatsapp_from_number_that_is_not_owned_by_your_account(get_whatsapp):
    """
    GIVEN a valid whatsapp object
    WHEN sending text from a number that is not owned by your account
    THEN assert error is not a valid, SMS-capable inbound phone number
    """
    t = get_whatsapp
    t.from_ = '+15005550007'

    with pytest.raises(MessageSendError) as resp:
        t.send()

    response = str(resp.value)
    assert '400' in response


##############################################################################
# TESTS: Send to
##############################################################################

@skip_if_on_travisCI
def test_whatsapp_cant_route_to_number(get_whatsapp):
    """
    GIVEN a valid whatsapp object
    WHEN sending text to number that whatsapp can't route to
    THEN assert error "to" number is not reachable via MMS
    """
    t = get_whatsapp
    t.to = '+15005550002'

    with pytest.raises(MessageSendError) as resp:
        t.send()

    response = str(resp.value)
    assert '400' in response
    assert ("The 'To' phone number: {}, is not currently reachable using the "
           "'From' phone number: {} via MMS.'.format(t.to, t.from_) in response")


##############################################################################
# TESTS: Authentication
##############################################################################

@skip_if_on_travisCI
def test_whatsapp_invalid_account_sid(get_whatsapp):
    """
    GIVEN a valid whatsapp object
    WHEN sending text with invalid account sid credential
    THEN assert error resource not found
    """
    t = get_whatsapp
    token = t.__dict__['_auth'][1]
    t.__dict__['_auth'] = ('invalid_sid', token)

    with pytest.raises(MessageSendError) as resp:
        t.send()

    response = str(resp.value)
    assert '404 ' in response
    assert ('The requested resource /2010-04-01/Accounts/invalid_sid/Messages.json '
           'was not found') in response


@skip_if_on_travisCI
def test_whatsapp_invalid_auth_token(get_whatsapp):
    """
    GIVEN a valid whatsapp object
    WHEN sending text with invalid authentication token
    THEN assert error auth token was incorrect
    """
    t = get_whatsapp
    sid = t.__dict__['_auth'][0]
    t.__dict__['_auth'] = (sid, 'invalid_token')

    with pytest.raises(MessageSendError) as resp:
        t.send()

    response = str(resp.value)
    assert '401' in response
    assert 'UNAUTHORIZED' in response
    assert 'Authenticate' in response
