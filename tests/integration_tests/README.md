##Integration tests for sending texts (Twilio API)

###Steps
1. Set up Twilio [test account](https://www.twilio.com/try-twilio)
    - get test credentials on the account setting of Twilio console
2. Create twilio profile named 'integration_tester' (using test sid and token)
    - 'integration_tester' is profile name that is automatically recognized by the tests
3. Run `pytest tests/integration_tests/test_int_text.py --verbose`

###Tests
Main use cases are inputs to Twilio object:
- send from number
- send to number
- message body
- authentication

Test cases for above use cases are taken from [Twilio API test reference](https://www.twilio.com/docs/iam/test-credentials)


For example in [this section](https://www.twilio.com/docs/iam/test-credentials#test-sms-messages),  
+15005550001 phone number is a test number that, when sending text from it, it generates 
response 'invalid number'.  
+15005550007 creates response 'This phone number is not owned by your account or is not
 SMS-capable.'  
+15005550006 is a number that passes all validation and is used for happy scenario.

One test case is a happy scenario (send from valid 'from' number to valid 'to' number, 
with message body and valid credentials). All other tests are negative tests asserting 
generated error based on invalid 'from' number, invalid authentication etc. 

###Test pathway
Each test phone number generates specific response from Twilio API. When tests run, 
test Twilio object is passed to send() method in text.py file's Twilio class. From there 
an API POST request is made to Twilio endpoint. When response is positive (201) it is 
returned. Happy test scenario parses the response and asserts that entered inputs match 
response values. In cases when response is negative (400 family) MessageSendError is 
raised. Tests pick up raised exception, parse it and assert on its content. 
