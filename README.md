# Messages: Create and send messages fast!
[![](https://img.shields.io/badge/built%20with-Python3-red.svg)](https://www.python.org/)
[![PyPI version](https://badge.fury.io/py/messages.svg)](https://badge.fury.io/py/messages)
[![](https://travis-ci.org/trp07/messages.svg?branch=master)](https://travis-ci.org/trp07/messages)
[![](https://coveralls.io/repos/github/trp07/messages/badge.svg?branch=master)](https://coveralls.io/github/trp07/messages?branch=master)
[![](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/trp07/messages/blob/master/LICENSE)
[![](https://messages-py.herokuapp.com/badge.svg)](https://messages-py.herokuapp.com)

![messages_words](https://user-images.githubusercontent.com/18299151/48576493-c0a68380-e925-11e8-9322-eb5bd67858a4.png)

## Purpose
- **Messages** is a package designed to make sending messages easy and efficient!
- **Messages** wraps various standard library module, third-party module, web app API calls, etc. all in one package and with a **consistent API** across all message types.
- **Messages** can send messages **asynchronously**.
- **Messages** can send messages via the **command-line interface**.


## Installation
**Python3 only**
```shell
$ pip install messages
```

## Documentation in the [Wiki](https://github.com/trp07/messages/wiki)

## Supported Messages
* [Email](https://github.com/trp07/messages/wiki/Email)
* [Telegram](https://github.com/trp07/messages/wiki/TelegramBot)
* [Twilio](https://github.com/trp07/messages/wiki/Twilio)
* [Slack](https://github.com/trp07/messages/wiki/Slack)
* [WhatsApp](https://github.com/trp07/messages/wiki/WhatsApp)
* **Read the [Wiki](https://github.com/trp07/messages/wiki) for usage**.


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
$ messages email myProfileName 'Hello,\n\tBuy more Bitcoin!' \
--to you@there.com \
--attach ./file.txt \
--attach ~/Documents/file2.pdf \
Message sent...
```

### **Read** the [Wiki](https://github.com/trp07/messages/wiki) for **more examples**


## Contributing Code

* **Help Wanted!**
* All contributions are welcome to build upon the package!
* If it's a **message**, add it to messages!
* Read the [Wiki](https://github.com/trp07/messages/wiki) for guidelines.
* Join the conversation in the [Messages Slack Team](https://messages-py.herokuapp.com)
