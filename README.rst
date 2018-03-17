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

.. image:: https://messages-py.herokuapp.com/badge.svg
    :target: https://messages-py.herokuapp.com


Join the conversation in the `Messages Slack Team <https://messages-py.herokuapp.com>`_


Purpose
-------
- **Messages** is a package designed to make sending messages easy!
- **Messages** incorporates various standard library module, third-party module, web app API calls, etc. all in one package.
- **Messages** can send messages *asynchronously*.


Installation
------------
.. code-block:: console

  $ pip install messages


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
- Whatever the community thinks is fun or interesting.


Examples
--------
**Email**

.. code-block:: python

    >>> from messages import Email
    >>> msg = 'Hello,\n\tTry this new package called "messages"!'
    >>> m = Email(from_='me@here.com',
                to='you@there.com',
                body=msg,
                attachments=['./file1.txt', '~/Documents/file2.pdf']
            )
    >>>
    >>> m.send()        # send synchronously
    >>> m.send_async()  # send asynchronously


**Read** the `Wiki <https://github.com/trp07/messages/wiki>`_ for **more examples**



Contributing
------------
- **Help Wanted!**
- All contributions are welcome to build upon the package!
- If it's a **message**, add it to messages!
- Read the `Wiki <https://github.com/trp07/messages/wiki>`_ for guidelines.
