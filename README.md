# Messages: Create and send messages fast!
[![](https://img.shields.io/badge/built%20with-Python3-red.svg)](https://www.python.org/)
[![PyPI version](https://badge.fury.io/py/messages.svg)](https://badge.fury.io/py/messages)
[![](https://app.travis-ci.com/HomeMadePy/messages.svg?branch=master)](https://travis-ci.com/HomeMadePy/messages)
[![](https://coveralls.io/repos/github/HomeMadePy/messages/badge.svg?branch=master)](https://coveralls.io/github/HomeMadePy/messages?branch=master)
[![](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/HomeMadePy/messages/blob/master/LICENSE)

![messages_words](https://user-images.githubusercontent.com/18299151/48576493-c0a68380-e925-11e8-9322-eb5bd67858a4.png)

## Purpose
- **Messages** is a package designed to make sending messages easy and efficient!
- **Messages** intends to be a _lightweight_ package with minimal dependencies.
- **Messages** with a **consistent API** across all message types. 

## Installation
**Python3 only**
```shell
$ pip install messages
```

## Documentation in the [Wiki](https://github.com/HomeMadePy/messages/wiki)

## Supported Messages
* [Email](https://github.com/HomeMadePy/messages/wiki/Email)
* [Telegram](https://github.com/HomeMadePy/messages/wiki/TelegramBot)
* [Twilio](https://github.com/HomeMadePy/messages/wiki/Twilio)
* [WhatsApp](https://github.com/HomeMadePy/messages/wiki/WhatsApp)
* **Read the [Wiki](https://github.com/HomeMadePy/messages/wiki) for usage**.


# Examples
## [Email](https://github.com/HomeMadePy/messages/wiki/Email)

```python
>>> from messages import Email
>>> msg = 'Hello,\n\tBuy more Bitcoin!'
>>> m = Email(
            from_='me@here.com',
            server='smtp.here.com',
            port=465,
            to='you@there.com',
            auth='p@ssw0rd',       
            body=msg,
            attachments=['./file1.txt', '~/Documents/file2.pdf'],
   )
>>>
>>> m.send()        
Message sent...
```

### **Read** the [Wiki](https://github.com/HomeMadePy/messages/wiki) for **more examples**


## Contributing Code

* **Help Wanted!**
* All contributions are welcome to build upon the package!
* If it's a **message**, add it to messages!
* Read the [Wiki](https://github.com/HomeMadePy/messages/wiki) for guidelines.
