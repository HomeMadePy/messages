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


Purpose
-------
- **Messages** is a package designed to make sending messages easy!
- **Messages** incorporates various standard library module, third-party module, web app API calls, etc. all in one package.


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


Upcoming Messages
-----------------
- Chats
    - WhatsApp
    - Slack


Examples
--------
**Email**

.. code-block:: python

    >>> from messages import Email
    >>> msg = 'Hello,\n\tTry this new package called "messages"!'
    >>> m = Email('smtp.gmail.com', 465, 'password', from_='me@here.com',
                  to='you@there.com', cc=None, bcc=None, subject='Hello',
                  body_text=msg, attachments=['./file1.txt', '~/Documents/file2.pdf'])
    >>> m.send()



**Text Message**

.. code-block:: python

    >>> from messages import Twilio
    >>> msg = 'Hello,\n\tTry this new package called "messages"!'
    >>> t = Twilio('api_acct_sid', 'api_auth_token', from_='+16198675309',
                   to='+16195551212', body=msg, media_url='https://imgs.xkcd.com/comics/python.png')
    >>> t.send()


Contributing
------------
- **Help Wanted!**
- All contributions are welcome to build upon the package!
- If it's a **message**, add it to messages!
- Please read `CONTRIBUTING <https://github.com/trp07/messages/blob/master/CONTRIBUTING.md>`_ for guidelines, as well as a `TODO List <https://github.com/trp07/messages/blob/master/TODO.md>`_ for ideas on where to get started.
