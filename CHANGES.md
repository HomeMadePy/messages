Change Log
==========
0.8.0
--------
- Reintegrates **async** messages sending with the *.send_async() method for each message type


0.7.2
--------
- Replaces **requests** with **httpx** as a dependency
- Requires **python 3.7+** from here on out


0.7.1
--------
- Updates documentation

0.7.0
--------
- Adds Poetry as the package installer/manager.
- Removes CLI, API, CONFIG modules and features due to unstable dependencies and feature creep
- Working to migrate documentation from the github wiki to readthedocs.


0.5.0
-----
- Adds support for **WhatsApp** via the [Twilio-WhatsApp API](https://www.twilio.com/docs/sms/whatsapp)
- Adds code formating with Black
- Removes __setattr__ from Message Interface (ABC) and instead uses a property factory defined in _utils.py


0.4.4
-----
- Changes CLI structure to break out each message type into its own subcommand
- Changes each message interface to accept an **auth** param instead of naming each credential param separately.  If a message requires more than one input for **auth**, then it will expect a tuple or a list.
- Redesigns the **_config.py** module to be more readable and easier
to interface with inside the message classes.


0.4.3
-----
- Adds **--verbose**, **-V** option to the CLI to enable verbose output for each message invocation.


0.4.2
-----
- Minor bug fix and document changes.


0.4.1
-----
- Adds a SlackPost class, for the [chat.postMessage](https://api.slack.com/methods/chat.postMessage) API
- Changes TelegramBot.get_chat_id method to not be called by __init__, instead as a manual method to be called by the user as needed since Telegram's getUpdate method clears all entries after 24-hours.


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


