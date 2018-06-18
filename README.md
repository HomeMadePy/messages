# Messages: Create and send messages fast!

[![](https://img.shields.io/badge/built%20with-Python3-red.svg)](https://www.python.org/)
[![PyPI version](https://badge.fury.io/py/messages.svg)](https://badge.fury.io/py/messages)
[![](https://travis-ci.org/trp07/messages.svg?branch=master)](https://travis-ci.org/trp07/messages)
[![](https://coveralls.io/repos/github/trp07/messages/badge.svg?branch=master)](https://coveralls.io/github/trp07/messages?branch=master)
[![](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/trp07/messages/blob/master/LICENSE)
[![](https://messages-py.herokuapp.com/badge.svg)](https://messages-py.herokuapp.com)

Join the conversation in the [Messages Slack Team](https://messages-py.herokuapp.com)

## Purpose

- **Messages** is a package designed to make sending messages easy!
- **Messages** wraps various standard library module, third-party module, web app API calls, etc. all in one package.
- **Messages** can send messages **asynchronously**.
- **Messages** can send messages via the **command-line interface**.


## Installation

```console
$ pip install messages
```

## Supported Messages

* [Email](https://github.com/trp07/messages/wiki/Email)
* [Telegram](https://github.com/trp07/messages/wiki/TelegramBot)
* [Twilio](https://github.com/trp07/messages/wiki/Twilio)
* [Slack](https://github.com/trp07/messages/wiki/Slack)
* Read the [Wiki](https://github.com/trp07/messages/wiki) for usage.


## Upcoming Messages

* Whatever the community thinks is fun or interesting.
* Please [Contribute](https://github.com/trp07/messages/wiki)!

# Examples

## [Email](https://github.com/trp07/messages/wiki/Email)

### REPL

```python
>>> from messages import Email
>>> msg = 'Hello,\n\tBuy more Bitcoin!'
>>> m = Email(
            from_='me@here.com',
            to='you@there.com',
            body=msg,
            attachments=['./file1.txt', '~/Documents/file2.pdf'],
            profile='myProfileName'
        )
>>>
>>> m.send()        # send synchronously
>>> m.send_async()  # send asynchronously
Message sent...
```

### CLI
```shell
$ messages email -t you@there.com \
-m 'Hello,\n\tBuy more Bitcoin!' \
-a ./file.txt \
-a ~/Documents/file2.pdf \
-P myProfileName
Message sent...
```

## [Telegram](https://github.com/trp07/messages/wiki/TelegramBot)

### REPL

```python
>>> from messages import TelegramBot
>>> msg = 'Hello,\n\tBuy more Bitcoin!'
>>> t = TelegramBot(
            chat_id='1234567',
            body=msg,
            attachments=['https://url1.com', 'https://url2.com'],
            profile='myProfileName'
        )
>>>
>>> t.send()        # send synchronously
>>> t.send_async()  # send asynchronously
Message sent...
```

### CLI
```shell
$ messages telegrambot \
-m 'Hello,\n\tBuy more Bitcoin!' \
-a 'https://url1.com/picture.gif' \
-a 'https://url2.com/file.pdf' \
-P myProfileName
Message sent...
```


### **Read** the [Wiki](https://github.com/trp07/messages/wiki) for **more examples**



## Contributing

* **Help Wanted!**
* All contributions are welcome to build upon the package!
* If it's a **message**, add it to messages!
* Read the [Wiki](https://github.com/trp07/messages/wiki) for guidelines.
