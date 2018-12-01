# Integration Testing
- This document discusses the end-to-end testing of each message class.
- The goal of integration testing is to ensure the most current version of _Messages_ properly implements the latest version of the specific service/api invoked in each module.
- As it stands, the integration test suite is not to run on CI build systems, such as Travis-CI, since user-specific credentials and test credentials are required to run the tests.
- Integration tests are run locally, by the developer, using their own credentials.

## Integration Testing Setup
In order to setup your work environment to perform integration testing, do the following:
1. First, ensure all unit-tests pass.
2. Configure each message class with `profile = integration_tester`, providing either real credentials or a set of test credentials.  See each message classes' sub-section for test credentials.  Each test file is guarded to not run if that message class wasn't configured in the **integration_tester** profile.
3. That's it.  Run the tests with `pytest --verbose`.  For each message class configured, as in step 2, the test file will automatically run.  For each message class not configured, the test file will automatically skip all included tests.

## Email
Integration testing not yet implemented

## Slack
Integration testing not yet implemented

## Telegram
Integration testing not yet implemented

## Twilio
### Test Credentials
1. Set up a Twilio [test account](https://www.twilio.com/try-twilio).
2. Get test credentials from the account setting of the Twilio console.
3. Ensure you configure twilio under the **integration_tester** profile with the credentials obstained in step 2.

### Tests
Main parameters tested, in-line with [Twilio API test reference](https://www.twilio.com/docs/iam/test-credentials):
- send `from_` number
- send `to` number
- message `body`
- authentication, `auth`

### Noteable Test API Input Parameters
- `from_ = +15005550006` used for happy-path testing.
- `from_ = +15005550001` generates an _invalid number_ response.
- `from_ = +15005550007` outputs _This phone number is not owned by your account or is not SMS-capable_.  

## WhatsApp
Integration testing not yet implemented
