import pytest
from messages.text import Twilio


##############################################################################
# FIXTURES
##############################################################################

@pytest.fixture()
def get_twilio(profile='mtwilio_test'):
    """Return a valid Twilio object."""
    t = Twilio(from_='+15005550006', to='+14159999999',
               body='test text!',
               attachments='https://imgs.xkcd.com/comics/python.png',
               profile=profile, save=False)
    return t


##############################################################################
# TESTS: Send from
##############################################################################

def test_01_text_successful(get_twilio):
    """
    GIVEN a valid Twilio object
    WHEN sending text message from valid number to valid number
    THEN assert response contains correct values
    """
    t = get_twilio
    resp = t.send()

    resp_dict = resp.json()
    assert resp.status_code == 201
    assert resp_dict['from'] == t.from_
    assert resp_dict['to'] == t.to
    assert resp_dict['body'] == t.body
    assert resp_dict['status'] == 'queued'
    assert resp_dict['error_message'] is None
    assert 'media' in resp_dict['subresource_uris']


def test_02_text_with_empty_body(get_twilio):
    """
    GIVEN a valid Twilio object
    WHEN sending text with empty body
    THEN assert error message body is required
    """
    t = get_twilio
    t.body = ''
    t.attachments = None

    resp = t.send()
    assert resp.status_code == 400
    resp_full = {
        'code': 21602,
        'message': 'Message body is required.',
        'more_info': 'https://www.twilio.com/docs/errors/21602',
        'status': 400}
    assert resp.json() == resp_full


def test_03_send_from_unavailable_number(get_twilio):
    """
    GIVEN a valid Twilio object
    WHEN sending text from unavailable number
    THEN assert error "from" number is not valid inbound phone number
    """
    t = get_twilio
    t.from_ = '+15005550000'

    resp = t.send()
    assert resp.status_code == 400
    resp_full = {
        "code": 21606,
        "message": "The From phone number +15005550000 is not a valid, "
                   "SMS-capable inbound phone number or short code for your account.",
        "more_info": "https://www.twilio.com/docs/errors/21606",
        "status": 400
    }
    assert resp.json() == resp_full


def test_04_send_from_invalid_number(get_twilio):
    """
    GIVEN a valid Twilio object
    WHEN sending text from invalid number
    THEN assert error "from" number is not valid phone number
    """
    t = get_twilio
    t.from_ = '+15005550001'

    resp = t.send()
    assert resp.status_code == 400
    resp_full = {
        "code": 21212,
        "message": "The 'From' number +15005550001 is not a valid phone number, "
                   "shortcode, or alphanumeric sender ID.",
        "more_info": "https://www.twilio.com/docs/errors/21212",
        "status": 400
    }
    assert resp.json() == resp_full


def test_05_send_from_another_invalid_number(get_twilio):
    """
    GIVEN a valid Twilio object
    WHEN sending text from a not valid sms-capable inbound number
    THEN assert error "from" number is not valid inbound phone number
    """
    t = get_twilio
    t.__dict__['from_'] = '+123'

    resp = t.send()
    assert resp.status_code == 400
    resp_full = {
        'code': 21606,
        'message': 'The From phone number +123 is not a valid, SMS-capable inbound '
                   'phone number or short code for your account.',
        'more_info': 'https://www.twilio.com/docs/errors/21606',
        'status': 400
    }
    assert resp.json() == resp_full


def test_06_text_from_number_that_is_not_owned_by_your_account(get_twilio):
    """
    GIVEN a valid Twilio object
    WHEN sending text from a number that is not owned by your account
    THEN assert error is not a valid, SMS-capable inbound phone number
    """
    t = get_twilio
    t.from_ = '+15005550007'

    resp = t.send()
    assert resp.status_code == 400

    resp_full = {
        "code": 21606,
        "message": "The From phone number +15005550007 is not a valid, SMS-capable "
                   "inbound phone number or short code for your account.",
        "more_info": "https://www.twilio.com/docs/errors/21606",
        "status": 400
    }
    assert resp.json() == resp_full


def test_07_text_from_full_sms_queue(get_twilio):
    """
    GIVEN a valid Twilio object
    WHEN sending text from a sms queue that is full
    THEN assert error SMS queue is full
    """
    t = get_twilio
    t.from_ = '+15005550008'

    resp = t.send()
    assert resp.status_code == 429

    resp_full = {
        "code": 21611,
        "message": "SMS queue is full.",
        "more_info": "https://www.twilio.com/docs/errors/21611",
        "status": 429
    }
    assert resp.json() == resp_full


##############################################################################
# TESTS: Send to
##############################################################################

def test_08_text_to_non_mobile_number(get_twilio):
    """
    GIVEN a valid Twilio object
    WHEN sending text to a non-mobile number
    THEN assert error "to" number is not a mobile number
    """
    t = get_twilio
    t.to = '+15005550009'

    resp = t.send()
    assert resp.status_code == 400

    resp_full = {
        "code": 21614,
        "message": "To number: +15005550009, is not a mobile number",
        "more_info": "https://www.twilio.com/docs/errors/21614",
        "status": 400
    }
    assert resp.json() == resp_full


def test_09_send_to_invalid_number(get_twilio):
    """
    GIVEN a valid Twilio object
    WHEN sending text to invalid number
    THEN assert error "to" number is not a valid phone number
    """
    t = get_twilio
    t.__dict__['to'] = '123'

    resp = t.send()
    assert resp.status_code == 400

    resp_full = {
        'code': 21211,
        'message': "The 'To' number 123 is not a valid phone number.",
        'more_info': 'https://www.twilio.com/docs/errors/21211',
        'status': 400
    }
    assert resp.json() == resp_full


def test_10_twilio_cant_route_to_number(get_twilio):
    """
    GIVEN a valid Twilio object
    WHEN sending text to number that Twilio can't route to
    THEN assert error "to" number is not reachable via MMS
    """
    t = get_twilio
    t.to = '+15005550002'

    resp = t.send()
    assert resp.status_code == 400

    resp_full = {
        'code': 21612,
        'message': "The 'To' phone number: +15005550002, is not currently reachable "
                   "using the 'From' phone number: +15005550006 via MMS.",
        'more_info': 'https://www.twilio.com/docs/errors/21612',
        'status': 400
    }
    assert resp.json() == resp_full


##############################################################################
# TESTS: Authentication
##############################################################################

def test_11_invalid_account_sid(get_twilio):
    """
    GIVEN a valid Twilio object
    WHEN sending text with invalid account sid credential
    THEN assert error resource not found
    """
    t = get_twilio
    token = t.__dict__['_auth'][1]
    t.__dict__['_auth'] = ('invalid_sid', token)

    resp = t.send()
    assert resp.status_code == 404

    resp_full = {
        'code': 20404,
        'message': 'The requested resource '
                   '/2010-04-01/Accounts/invalid_sid/Messages.json was not found',
        'more_info': 'https://www.twilio.com/docs/errors/20404',
        'status': 404
    }
    assert resp.json() == resp_full


def test_12_invalid_auth_token(get_twilio):
    """
    GIVEN a valid Twilio object
    WHEN sending text with invalid authentication token
    THEN assert error auth token was incorrect
    """
    t = get_twilio
    sid = t.__dict__['_auth'][0]
    t.__dict__['_auth'] = (sid, 'invalid_token')

    resp = t.send()
    assert resp.status_code == 401

    resp_full = {
        'code': 20003,
        'detail': 'Your AccountSid or AuthToken was incorrect.',
        'message': 'Authenticate',
        'more_info': 'https://www.twilio.com/docs/errors/20003',
        'status': 401
    }
    assert resp.json() == resp_full
