Messages: Create and send messages fast!
========================================

.. image:: https://img.shields.io/badge/built%20with-Python3-red.svg
    :target: https://www.python.org/

.. image:: https://travis-ci.org/trp07/messages.svg?branch=master
    :target: https://travis-ci.org/trp07/messages

.. image:: https://coveralls.io/repos/github/trp07/messages/badge.svg?branch=master
    :target: https://coveralls.io/github/trp07/messages?branch=master

.. image:: https://img.shields.io/badge/license-MIT-blue.svg
    :target: https://github.com/trp07/messages/blob/master/LICENSE


Join the conversation in the `Messages Slack Team <https://messages-py.slack.com>`_


Purpose
-------
- **Messages** is a package designed to make sending messages easy!
- **Messages** incorporates various standard library module, third-party module, web app API calls, etc. all in one package.
- **Messages** can send messages asynchronously.


Installation
------------
.. code-block:: console

  $ pip install git+https://github.com/trp07/messages


Supported Messages
------------------
- Email
    - SMTP

- Text Messages (SMS/MMS)
    - Twilio API (must have API keys)

- Slack
    - Inbound Webhook API


Upcoming Messages
-----------------
- WhatsApp


Examples
--------
**Email**

.. code-block:: python

    >>> from messages import Email
    >>> msg = 'Hello,\n\tTry this new package called "messages"!'
    >>> m = Email('smtp.gmail.com', 465, 'password', from_='me@here.com',
                  to='you@there.com', cc=None, bcc=None, subject='Hello',
                  body=msg, attachments=['./file1.txt', '~/Documents/file2.pdf'])
    >>>
    >>> m.send()        # send synchronously
    >>> m.send_async()  # send asynchronously



**Text Message**

.. code-block:: python

    >>> from messages import Twilio
    >>> msg = 'Hello,\n\tTry this new package called "messages"!'
    >>> t = Twilio('api_acct_sid', 'api_auth_token', from_='+16198675309',
                   to='+16195551212', body=msg, media_url='https://imgs.xkcd.com/comics/python.png')
    >>>
    >>> t.send()        # send synchronously
    >>> t.send_async()  # send asynchronously



**Slack - Inbound Webhook API**

.. code-block:: python

    >>> from messages import SlackWebhook
    >>> msg = 'Hello,\n\tTry this new package called "messages"!'
    >>> s = SlackWebhook('webhook_url', body=msg, attach_urls='https://imgs.xkcd.com/comics/python.png')
    >>>
    >>> s.send()        # send synchronously
    >>> s.send_async()  # send asynchronously


Contributing
------------
- **Help Wanted!**
- All contributions are welcome to build upon the package!
- If it's a **message**, add it to messages!
- Please read `CONTRIBUTING <https://github.com/trp07/messages/wiki/CONTRIBUTING>`_ for guidelines, as well as a `TODO List <https://github.com/trp07/messages/wiki/TODO>`_ for ideas on where to get started.
