Change Log
==========

0.3.0
-----
- Completes CLI functionality
    - However, this may undergo some modification


0.2.0
-----
- Changes the message class interface to be more consistent with eachother.
- Adds the ability to create config.json files to save default parameters and credentials.
- Adds an **api.py** module to make sending messages more user friendly.


0.1.2
-----
- Adds input validation via the `validus <https://github.com/shopnilsazal/validus>`_ package, which uses regular expressions to verify formatting (i.e. email addresses, urls, etc).


0.1.1
-----
- Adds **Slack Inbound Webhook API** functionality via **SlackWebhook** class.
- Incorporates **attrs** package for code brevity.


0.1.0
-----
- Adds **asynchronous** message sending via send_async() method.


0.0.0
-----
- Initial release.
- Supported Messages:
    - Email - SMTP
    - SMS/MMS - Twilio
