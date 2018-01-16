Messages: Create and send messages fast!
========================================

.. image:: https://img.shields.io/badge/built%20with-Python3-red.svg
    :target: https://www.python.org/

.. image:: https://travis-ci.org/trp07/messages.svg?branch=master
    :target: https://travis-ci.org/trp07/messages

.. image:: https://coveralls.io/repos/github/trp07/messages/badge.svg?branch=master
    :target: https://coveralls.io/github/messages/messages?branch=master

.. image:: https://img.shields.io/badge/license-MIT-blue.svg
    :target: https://github.com/trp07/messages/master/LICENSE


**Messages** is a package designed to make sending messages easy and efficient!


Installation
------------
.. code-block:: console

  $ pip install git+https://github.com/trp07/messages


Supported Messages
------------------
- Email
    - SMTP

- Text Messages (SMS/MMS)
    - Twilio API


Upcoming Messages
-----------------
- Chats
    - WhatsApp
    - Slack


Usage
-----
Email

.. code-block:: python

    >>> from messages import Email
    >>> msg = 'Hello,\n\tTry this new package called "messages"!'
    >>> m = Email('smtp.google.com', 465, 'password', From='me@here.com',
                  To='you@there.com', Cc=None, Bcc=None, subject='Hello',
                  body_text=msg, attachments=['./file1.txt', '~/Documents/file2.pdf'])
    >>> m.send()



Text Message

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
- Please read `CONTRIBUTING <https://github.com/trp07/messages/master/CONTRIBUTING.md>`_ for guidelines.
