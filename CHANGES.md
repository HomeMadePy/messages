Change Log
==========

Current Progress
----------------
-   Next version in development

0.4.0
-----
-   Adds support for [Telegram Bot](https://core.telegram.org/bots/api#available-methods) messages
-   Makes config.py and exceptions.py into private _*.py modules


0.3.4
-----

-   Changes README.rst to README.md since now compatible on PyPI
-   Reworked the \_utils.py module to be more functional and readable
-   Removes the twilio sdk dependency and just uses the requests library

0.3.3
-----

-   Enforces python \>= 3.5 for install
-   Tweaks CLI args a bit for ease of use
-   Adds more information to messages --help and docstrings for cli use

0.3.2
-----

-   Adds a **-C**, **--configure** option to the CLI in order to
    configure and create an entry in the config.json file for a specific
    message type. That way default parameters and credentials can be
    saved away for easier use later.

0.3.1
-----

-   Moves documenation to the github Wiki and trims down the README

0.3.0
-----

-   Completes CLI functionality
    :   -   However, this may undergo some modification

0.2.0
-----

-   Changes the message class interface to be more consistent with
    eachother.
-   Adds the ability to create config.json files to save default
    parameters and credentials.
-   Adds an **api.py** module to make sending messages more user
    friendly.

0.1.2
-----

-   Adds input validation via the
    [validus](https://github.com/shopnilsazal/validus) package, which
    uses regular expressions to verify formatting (i.e. email addresses,
    urls, etc).

0.1.1
-----

-   Adds **Slack Inbound Webhook API** functionality via
    **SlackWebhook** class.
-   Incorporates **attrs** package for code brevity.

0.1.0
-----

-   Adds **asynchronous** message sending via send\_async() method.

0.0.0
-----

-   Initial release.
-   Supported Messages:
        -   Email - SMTP
        -   SMS/MMS - Twilio


