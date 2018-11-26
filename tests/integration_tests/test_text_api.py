import pytest
import unittest
from messages.text import Twilio
import os


class TwilioApiTest(unittest.TestCase):

    def setUp(self):
        self.base_url = 'https://api.twilio.com/2010-04-01/Accounts'

    ###############################################################################
    # From
    ###############################################################################
    # DONE
    def test_01_text_successful(self):
        self.test_account_sid = os.getenv('TEST_ACCOUNT_SID')

        t = Twilio(from_='+15005550006', to='+14159999999',
                   body='Test text from Twillio messages object!',
                   attachments='https://imgs.xkcd.com/comics/python.png',
                   profile='mtwilio_test', save=False)

        resp = t.send()
        resp_dict = resp.json()
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp_dict['account_sid'], self.test_account_sid)
        self.assertEqual(resp_dict['from'], t.from_)
        self.assertEqual(resp_dict['to'], t.to)
        self.assertEqual(resp_dict['body'], t.body)
        self.assertEqual(resp_dict['status'], 'queued')
        self.assertEqual(resp_dict['error_message'], None)
        self.assertIn('media', resp_dict['subresource_uris'])

    # TODO - NOT DONE - INCORRECT - SHOULD THROW ERROR ABOUT MISSING BODY
    def test_02_text_with_empty_body(self):
        t = Twilio(from_='+15005550006', to='+14159999999',
                   body='',
                   attachments='https://imgs.xkcd.com/comics/python.png',
                   profile='mtwilio_test', save=False)

        resp = t.send()
        resp_dict = resp.json()
        self.assertEqual(resp.status_code, 400)

    # DONE
    def test_03_send_from_unavailable_number(self):
        t = Twilio(from_='+15005550000', to='+14159999999',
                   body='',
                   attachments='https://imgs.xkcd.com/comics/python.png',
                   profile='mtwilio_test', save=False)

        resp = t.send()
        resp_dict = resp.json()
        self.assertEqual(resp.status_code, 400)
        resp_full = {
            "code": 21606,
            "message": "The From phone number +15005550000 is not a valid, "
                       "SMS-capable inbound phone number or short code for your account.",
            "more_info": "https://www.twilio.com/docs/errors/21606",
            "status": 400
        }
        self.assertEqual(resp_dict, resp_full)

    # DONE
    def test_04_send_from_invalid_number(self):
        t = Twilio(from_='+15005550001', to='+14159999999',
                   body='',
                   attachments='https://imgs.xkcd.com/comics/python.png',
                   profile='mtwilio_test', save=False)

        resp = t.send()
        resp_dict = resp.json()
        self.assertEqual(resp.status_code, 400)
        resp_full = {
            "code": 21212,
            "message": "The 'From' number +15005550001 is not a valid phone number, "
                       "shortcode, or alphanumeric sender ID.",
            "more_info": "https://www.twilio.com/docs/errors/21212",
            "status": 400
        }
        self.assertEqual(resp_dict, resp_full)

    # DONE
    def test_05_send_from_another_invalid_number(self):
        """Completely invalid "from_" number"""
        t = Twilio(from_='+15005550000', to='+14159999999',
                   body='',
                   attachments='https://imgs.xkcd.com/comics/python.png',
                   profile='mtwilio_test', save=False)

        t.__dict__['to'] = '123'

        resp = t.send()
        resp_dict = resp.json()
        self.assertEqual(resp.status_code, 400)
        resp_full = {
            'code': 21606,
            'message': 'The From phone number +15005550000 is not a valid, SMS-capable '
                       'inbound phone number or short code for your account.',
            'more_info': 'https://www.twilio.com/docs/errors/21606', 'status': 400
        }
        self.assertEqual(resp_dict, resp_full)

    # DONE  - TODO - CHECK DOES IT THROW EXCEPTION IN REAL TWILIO TEST?
    def test_06_text_from_number_that_is_not_owned_by_your_account(self):
        """This phone number is not owned by your account or is not SMS-capable.
         +15005550007"""
        t = Twilio(from_='+15005550007', to='+14159999999',
                   body='',
                   attachments='https://imgs.xkcd.com/comics/python.png',
                   profile='mtwilio_test', save=False)

        resp = t.send()
        resp_dict = resp.json()
        self.assertEqual(resp.status_code, 400)

        resp_full = {
            "code": 21606,
            "message": "The From phone number +15005550007 is not a valid, SMS-capable "
                       "inbound phone number or short code for your account.",
            "more_info": "https://www.twilio.com/docs/errors/21606",
            "status": 400
        }
        self.assertEqual(resp_dict, resp_full)

    # DONE
    def test_07_text_from_full_sms_queue(self):
        """This number has an SMS message queue that is full. +15005550008"""
        t = Twilio(from_='+15005550008', to='+14159999999',
                   body='',
                   attachments='https://imgs.xkcd.com/comics/python.png',
                   profile='mtwilio_test', save=False)

        resp = t.send()
        resp_dict = resp.json()
        self.assertEqual(resp.status_code, 429)
        resp_full = {
            "code": 21611,
            "message": "SMS queue is full.",
            "more_info": "https://www.twilio.com/docs/errors/21611",
            "status": 429
        }
        self.assertEqual(resp_dict, resp_full)

    ###############################################################################
    # To
    ###############################################################################

    # DONE
    def test_08_text_to_non_mobile_number(self):
        """This number is incapable of receiving SMS messages because it's a non-mobile
            number. +15005550009. In real twilio account this only applies to countries
            other than US, UK and Canada."""
        t = Twilio(from_='+15005550006', to='+15005550009',
                   body='Test text from Twillio messages object!',
                   attachments='https://imgs.xkcd.com/comics/python.png',
                   profile='mtwilio_test', save=False)

        resp = t.send()
        resp_dict = resp.json()
        self.assertEqual(resp.status_code, 400)
        resp_full = {
            "code": 21614,
            "message": "To number: +15005550009, is not a mobile number",
            "more_info": "https://www.twilio.com/docs/errors/21614",
            "status": 400
        }
        self.assertEqual(resp_dict, resp_full)

        # TODO Except for empty message body - that works in both, error is caught in
        #  both test and real twilio

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
