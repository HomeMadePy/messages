# Messages: Create and send messages fast!

[![](https://img.shields.io/badge/built%20with-Python3-red.svg)](https://www.python.org/)
[![](https://travis-ci.org/trp07/messages.svg?branch=master)](https://travis-ci.org/trp07/messages)
[![](https://coveralls.io/repos/github/trp07/messages/badge.svg?branch=master)](https://coveralls.io/github/trp07/messages?branch=master)
[![](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/trp07/messages/blob/master/LICENSE)
[![](https://messages-py.herokuapp.com/badge.svg)](https://messages-py.herokuapp.com)

Join the conversation in the [Messages Slack Team](https://messages-py.herokuapp.com)

## Purpose

- **Messages** is a package designed to make sending messages easy!
- **Messages** incorporates various standard library module, third-party module, web app API calls, etc. all in one package.
- **Messages** can send messages *asynchronously*.


## Installation

```console
$ pip install messages
```

## Supported Messages

* [Email SMTP](https://github.com/trp07/messages/wiki/Email)
* [Twilio](https://github.com/trp07/messages/wiki/Twilio)
* [Slack](https://github.com/trp07/messages/wiki/Slack_IncomingWebhook)
* Read the [Wiki](https://github.com/trp07/messages/wiki) for usage.


## Upcoming Messages

* Whatever the community thinks is fun or interesting.

## Examples

### Email

```python
>>> from messages import Email
>>> msg = 'Hello,\n\tTry this new package called "messages"!'
>>> m = Email(from_='me@here.com',
            to='you@there.com',
            body=msg,
            attachments=['./file1.txt', '~/Documents/file2.pdf'],
            profile='myProfileName'
        )
>>>
>>> m.send()        # send synchronously
>>> m.send_async()  # send asynchronously
```

**Read** the [Wiki](https://github.com/trp07/messages/wiki) for **more examples**



## Contributing

* **Help Wanted!**
* All contributions are welcome to build upon the package!
* If it's a **message**, add it to messages!
* Read the [Wiki](https://github.com/trp07/messages/wiki) for guidelines.
