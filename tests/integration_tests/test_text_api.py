"""TODO - add 8 more tests (do these later) [test use cases: from, to, area code,
        credentials, attachment]
        - add test that raises HTTPrequestsError
        - put Twillio object into setUp to only write it once and then override
        phone numbers (t.to = ..., t.from = ...)
        - change unittest to pytest
        - figure out why 'empty body' test isn't working
        - write docstring GIVE, WHEN, THEN under each test - formata per other tests
        - rename tests to as used in other tests if necessary
        - cleanup"""

from messages.text import Twilio


###############################################################################
# From
###############################################################################
def test_01_text_successful():
    """
    GIVEN a valid Twilio object
    WHEN the sends text message fromvalid number to valid number
    THEN assert response contains correct values
    """
    t = Twilio(from_='+15005550006', to='+14159999999',
               body='Test text from Twillio messages object!',
               attachments='https://imgs.xkcd.com/comics/python.png',
               profile='mtwilio_test', save=False)

    resp = t.send()
    resp_dict = resp.json()
    assert resp.status_code == 201
    assert resp_dict['from'] == t.from_
    assert resp_dict['to'] == t.to
    assert resp_dict['body'] == t.body
    assert resp_dict['status'] == 'queued'
    assert resp_dict['error_message'] is None
    assert 'media' in resp_dict['subresource_uris']

def test_02_text_with_empty_body():
    t = Twilio(from_='+15005550006', to='+14159999999',
               body='',
               attachments='https://imgs.xkcd.com/comics/python.png',
               profile='mtwilio_test', save=False)

    resp = t.send()
    resp_dict = resp.json()
    assert resp.status_code == 400

def test_03_send_from_unavailable_number():
    t = Twilio(from_='+15005550000', to='+14159999999',
               body='Text from unavailable number.',
               attachments='https://imgs.xkcd.com/comics/python.png',
               profile='mtwilio_test', save=False)

    resp = t.send()
    resp_dict = resp.json()
    assert resp.status_code == 400
    resp_full = {
        "code": 21606,
        "message": "The From phone number +15005550000 is not a valid, "
                   "SMS-capable inbound phone number or short code for your account.",
        "more_info": "https://www.twilio.com/docs/errors/21606",
        "status": 400
    }
    assert resp_dict == resp_full

def test_04_send_from_invalid_number():
    t = Twilio(from_='+15005550001', to='+14159999999',
               body='Text from invalid number.',
               attachments='https://imgs.xkcd.com/comics/python.png',
               profile='mtwilio_test', save=False)

    resp = t.send()
    resp_dict = resp.json()
    assert resp.status_code == 400
    resp_full = {
        "code": 21212,
        "message": "The 'From' number +15005550001 is not a valid phone number, "
                   "shortcode, or alphanumeric sender ID.",
        "more_info": "https://www.twilio.com/docs/errors/21212",
        "status": 400
    }
    assert resp_dict == resp_full

def test_05_send_from_another_invalid_number():
    """Completely invalid "from_" number"""
    t = Twilio(from_='+15005550001', to='+14159999999',
               body='Text from another invalid number.',
               attachments='https://imgs.xkcd.com/comics/python.png',
               profile='mtwilio_test', save=False)

    t.__dict__['from_'] = '+123'

    resp = t.send()
    resp_dict = resp.json()
    assert resp.status_code == 400
    resp_full = {
        'code': 21606,
        'message': 'The From phone number +123 is not a valid, SMS-capable inbound '
                   'phone number or short code for your account.',
        'more_info': 'https://www.twilio.com/docs/errors/21606',
        'status': 400
    }
    assert resp_dict == resp_full


# DONE  - TODO - CHECK DOES IT THROW EXCEPTION IN REAL TWILIO TEST? - DOESN'T
def test_06_text_from_number_that_is_not_owned_by_your_account():
    """This phone number is not owned by your account or is not SMS-capable.
     +15005550007"""
    t = Twilio(from_='+15005550007', to='+14159999999',
               body='',
               attachments='https://imgs.xkcd.com/comics/python.png',
               profile='mtwilio_test', save=False)

    resp = t.send()
    resp_dict = resp.json()
    assert resp.status_code == 400

    resp_full = {
        "code": 21606,
        "message": "The From phone number +15005550007 is not a valid, SMS-capable "
                   "inbound phone number or short code for your account.",
        "more_info": "https://www.twilio.com/docs/errors/21606",
        "status": 400
    }
    assert resp_dict == resp_full

def test_07_text_from_full_sms_queue():
    """This number has an SMS message queue that is full. +15005550008"""
    t = Twilio(from_='+15005550008', to='+14159999999',
               body='',
               attachments='https://imgs.xkcd.com/comics/python.png',
               profile='mtwilio_test', save=False)

    resp = t.send()
    resp_dict = resp.json()
    assert resp.status_code == 429

    resp_full = {
        "code": 21611,
        "message": "SMS queue is full.",
        "more_info": "https://www.twilio.com/docs/errors/21611",
        "status": 429
    }
    assert resp_dict == resp_full

###############################################################################
# To
###############################################################################
def test_08_text_to_non_mobile_number():
    """This number is incapable of receiving SMS messages because it's a non-mobile
        number. +15005550009. In real twilio account this only applies to countries
        other than US, UK and Canada."""
    t = Twilio(from_='+15005550006', to='+15005550009',
               body='Test text from Twillio messages object!',
               attachments='https://imgs.xkcd.com/comics/python.png',
               profile='mtwilio_test', save=False)

    resp = t.send()
    resp_dict = resp.json()
    assert resp.status_code == 400

    resp_full = {
        "code": 21614,
        "message": "To number: +15005550009, is not a mobile number",
        "more_info": "https://www.twilio.com/docs/errors/21614",
        "status": 400
    }
    assert resp_dict == resp_full

def test_09_send_to_invalid_number():
    """Completely invalid "from_" number"""
    t = Twilio(from_='+15005550006', to='+14159999999',
               body='Text from another invalid number.',
               attachments='https://imgs.xkcd.com/comics/python.png',
               profile='mtwilio_test', save=False)

    t.__dict__['to'] = '123'

    resp = t.send()
    resp_dict = resp.json()
    assert resp.status_code == 400

    resp_full = {
        'code': 21211,
        'message': "The 'To' number 123 is not a valid phone number.",
        'more_info': 'https://www.twilio.com/docs/errors/21211',
        'status': 400
    }
    assert resp_dict == resp_full

###############################################################################
# AUTHENTICATION
###############################################################################
def test_10_invalid_account_sid():
    """Completely invalid "from_" number"""
    t = Twilio(from_='+15005550006', to='+14159999999',
               body='Text from another invalid number.',
               attachments='https://imgs.xkcd.com/comics/python.png',
               profile='mtwilio_test', save=False)

    token = t.__dict__['_auth'][1]
    t.__dict__['_auth'] = ('invalid_sid', token)

    resp = t.send()
    resp_dict = resp.json()
    assert resp.status_code == 404

    resp_full = {
        'code': 20404,
        'message': 'The requested resource '
                   '/2010-04-01/Accounts/invalid_sid/Messages.json was not found',
        'more_info': 'https://www.twilio.com/docs/errors/20404',
        'status': 404
    }
    assert resp_dict == resp_full

def test_11_invalid_auth_token():
    """Completely invalid "from_" number"""
    t = Twilio(from_='+15005550006', to='+14159999999',
               body='Text from another invalid number.',
               attachments='https://imgs.xkcd.com/comics/python.png',
               profile='mtwilio_test', save=False)

    sid = t.__dict__['_auth'][0]
    t.__dict__['_auth'] = (sid, 'invalid_token')

    resp = t.send()
    resp_dict = resp.json()
    assert resp.status_code == 401

    resp_full = {
        'code': 20003,
        'detail': 'Your AccountSid or AuthToken was incorrect.',
        'message': 'Authenticate',
        'more_info': 'https://www.twilio.com/docs/errors/20003',
        'status': 401
    }
    assert resp_dict == resp_full


# TODO ADD THESE TESTS (TO)
# This phone number is invalid. +15005550001
# Twilio cannot route to this number. +15005550002
# Your account doesn't have the international permissions necessary to SMS this
# number. +15005550003
# This number is blacklisted for your account. +15005550004
# This number is incapable of receiving SMS messages. +15005550009
# Any other phone number is validated normally. All other numbers

###############################################################################
# Area code
###############################################################################
# This area code doesn't have any available phone numbers.
# This area code has an available number. (no error)
