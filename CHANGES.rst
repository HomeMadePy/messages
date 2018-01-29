Change Log
==========

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
