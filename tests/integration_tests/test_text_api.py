import pytest
import requests
import json
from requests.auth import HTTPBasicAuth
import unittest
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

import messages.text
from messages.text import Twilio
from messages.text import check_config_file
from messages._eventloop import MESSAGELOOP
from messages._exceptions import MessageSendError
from messages._exceptions import InvalidMessageInputError


import os


class TwilioApiTest(unittest.TestCase):

    def setUp(self):
        self.base_url = 'https://api.twilio.com/2010-04-01/Accounts'
        self.session = requests.Session()

        # TODO - get credentials from user's jsonconfig

        self.test_account_sid = os.getenv('TEST_ACCOUNT_SID')
        self.test_auth_token = os.getenv('TEST_AUTH_TOKEN')

        # self.account_sid = os.getenv('ACCOUNT_SID')
        # self.auth_token = os.getenv('AUTH_TOKEN')

    def test_01_sending_using_external_twilio_library(self):
        # self.client = Client(self.test_account_sid, self.test_auth_token)
        #
        # message = self.client.messages.create(
        #     body='Test test message',
        #     from_='+15005550006',
        #     to='+14159999999'
        # )
        # self.assertIsNotNone(message.sid)
        # self.assertIsInstance(message.sid, str)
        # self.assertEqual(message.body, 'Test test message')
        # self.assertEqual(message.status, 'queued')
        pass

    def test_02_sending_using_requests(self):
        """Basic auth on client side Using requests HTTPBasicAuth module"""
        # twilio_headers = {
        #     'Content-Type': 'application/x-www-form-urlencoded',
        #     'WWW - Authenticate': 'Basic realm = "Twilio API'
        # }
        #
        # payload = {
        #     'Body': 'test message from requests',
        #     'To': '+14159999999',
        #     'From': '+15005550006'}
        #
        # url = self.base_url + f'/{self.test_account_sid}' + '/Messages.json'
        #
        # r = self.session.post(url, data=payload, headers=twilio_headers,
        #                       auth=HTTPBasicAuth(self.test_account_sid, self.test_auth_token))
        #
        # resp = r.json()
        #
        # self.assertEqual(r.status_code, 201)
        # self.assertEqual(resp['body'], 'test message from requests')
        pass


    ###############################################################################
    # From
    ###############################################################################
    # from https://www.twilio.com/docs/iam/test-credentials?code-sample=code-attempt-to-send-a-message-with-an-empty-sms-body&code-language=Python&code-sdk-version=6.x

    def test_03_text_successful(self):
        # TODO get credentials from jsonconfig
        # TODO determine meaningful test cases

        t = Twilio(from_='+15005550006', to='+14159999999',
                   auth=(self.test_account_sid, self.test_auth_token),
                   body='Test text from Twillio messages object!',
                   attachments='https://imgs.xkcd.com/comics/python.png',
                   profile='mtwilio', save=False)

        resp = t.send()
        resp_dict = resp.json()
        print(json.dumps(resp_dict, indent=2))

        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp_dict['account_sid'], self.test_account_sid)
        self.assertEqual(resp_dict['from'], t.from_)
        self.assertEqual(resp_dict['to'], t.to)
        self.assertEqual(resp_dict['body'], t.body)
        self.assertEqual(resp_dict['status'], 'queued')
        self.assertEqual(resp_dict['error_message'], None)
        self.assertIn('media', resp_dict['subresource_uris'])

    def test_04_text_with_empty_body(self):
        # TODO get credentials from jsonconfig
        # TODO determine meaningful test cases

        t = Twilio(from_='+15005550006', to='+14159999999',
                   auth=(self.test_account_sid, self.test_auth_token),
                   body='',
                   attachments='https://imgs.xkcd.com/comics/python.png',
                   profile='mtwilio', save=False)

        resp = t.send()
        resp_dict = resp.json()
        self.assertEqual(resp.status_code, 201)
        print(json.dumps(resp_dict, indent=2))
        # self.assertEqual(resp.error_code, 400)
        # self.assertRaises(requests.exceptions.HTTPError)
        # self.assertRaises(MessageSendError)

    def test_05_send_from_unavailable_number(self):
        # TODO get credentials from jsonconfig
        # TODO determine meaningful test cases

        t = Twilio(from_='+15005550000', to='+14159999999',
                   auth=(self.test_account_sid, self.test_auth_token),
                   body='',
                   attachments='https://imgs.xkcd.com/comics/python.png',
                   profile='mtwilio', save=False)

        resp = t.send()

        self.assertEqual(resp.status, 400)
        self.assertRaises(InvalidMessageInputError) # <-- FALSE POSITIVE
        self.assertRaises(IndexError)   # TODO <------ NOT WORKING, NOT ASSERTING FALSE
        self.assertEqual(type(resp), TwilioRestException)
        self.assertRaises(TwilioRestException)


    def test_06_send_from_invalid_number(self):
        # TODO get credentials from jsonconfig
        # TODO determine meaningful test cases

        t = Twilio(from_='+15005550001', to='+14159999999',
                   auth=(self.test_account_sid, self.test_auth_token),
                   body='',
                   attachments='https://imgs.xkcd.com/comics/python.png',
                   profile='mtwilio', save=False)

        resp = t.send()
        self.assertRaises(TwilioRestException)

    # I'd like to catch the internal validation exception here
    def test_06_send_from_invalid_number_2(self):
        """Completely invalid "from_" number"""
        t = Twilio(from_='+123', to='+14159999999',
                   auth=(self.test_account_sid, self.test_auth_token),
                   body='',
                   attachments='https://imgs.xkcd.com/comics/python.png',
                   profile='mtwilio', save=False)

        # from messages._utils import validate_twilio
        # try:
        #     validate_twilio('from_', '+123')
        # except InvalidMessageInputError as e:
        #     self.assertRaises(InvalidMessageInputError)


        resp = t.send()
        self.assertEqual(resp.status, 400)
        self.assertRaises(InvalidMessageInputError) # <----- DOES NOT SEERT THE
        # EXCEPTION - NOT WORKING !!!! - EMPTY
        print(type(resp))

    # TODO - PASSES REAL TWILIO TEST
    def test_07_text_from_number_that_is_not_owned_by_your_account(self):
        """This phone number is not owned by your account or is not SMS-capable.
         +15005550007"""
        t = Twilio(from_='+15005550007', to='+14159999999',
                   auth=(self.test_account_sid, self.test_auth_token),
                   body='',
                   attachments='https://imgs.xkcd.com/comics/python.png',
                   profile='mtwilio', save=False)

        resp = t.send()
        self.assertRaises(TwilioRestException)

    def test_08_text_from_full_sms_queue(self):
        """This number has an SMS message queue that is full. +15005550008"""
        t = Twilio(from_='+15005550008', to='+14159999999',
                   auth=(self.test_account_sid, self.test_auth_token),
                   body='',
                   attachments='https://imgs.xkcd.com/comics/python.png',
                   profile='mtwilio', save=False)

        resp = t.send()
        self.assertRaises(TwilioRestException)

    ###############################################################################
    # To
    ###############################################################################

    # TODO - SORT OF PASSES REAL TWILIO TEST - NOT APPLICABLE TO US NUMBERS
    def test_09_text_to_non_mobile_number(self):
        """This number is incapable of receiving SMS messages. +15005550009
            In real twilio account this tnly applies to countries other than US,
            UK and Canada."""
        t = Twilio(from_='+15005550006', to='+15005550009',
                   auth=(self.test_account_sid, self.test_auth_token),
                   body='Test text from Twillio messages object!',
                   attachments='https://imgs.xkcd.com/comics/python.png',
                   profile='mtwilio', save=False)

        resp = t.send()
        self.assertRaises(TwilioRestException)
        self.assertEqual(resp.status, 400)

        # 1
        # TODO - the problem is that all these tests catch errors, but when use
        # TODO   these scenarios on real twilio account, error  ARE NOT CUGHT!
        # for example: sending to - non-mobile number throws error in test twilio
        # but it doesn't when i send text to non-mobile number from my real twilio !!
        # TODO Except for empty message body - that works in both, error is caught in
        #  both test and real twilio

        # 2
        # WHY I'M USING TWILIO API LIBRARY:
        # When wtilioRestException is hit and MEssageSendException is raise on it,
        # the custome message doesn't seem to work. I keep geeting  ugly full blown
        # twilio error message.
        # in case of get_session methos it worked fine:
        # except SMTPResponseException as e:
        #     raise MessageSendError(e.smtp_error.decode("unicode_escape"))
        # but it doesn;t seem to work with twilio exception.

        # 3
        # OVERLAPPING VALIDATION ERROR HANDLING: 1. BUILT-IN VALIDUS ONE, AND TWILIO ONE



        # self.assertEqual(TwilioRestException.args[0] )

        # self.assertEqual(resp.error_code , 400)
        # self.assertRaises(requests.exceptions.HTTPError)
        # self.assertRaises(MessageSendError)


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





