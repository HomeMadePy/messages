"""
Utility Module - globals, classes, and functions useful to all other modules.

1.  Validator
    - Class used to validate user input for each message class.
    - i.e. validate email address inputs or phone number inputs
        using regular expressions.
    - Uses the third-party module, 'validus', for regular expressions.
        https://github.com/shopnilsazal/validus
"""

import functools
import inspect

import validus

from .exceptions import InvalidMessageInputError


class Validator:
    """
    Input validation class.

    Each message classe's 'command' should be a command that returns a bool.
    """

    EMAIL = {
             'from_': {
                       'command': validus.isemail,
                       'type': 'email address',
                       },
             'to': {
                    'command': validus.isemail,
                    'type': 'email address',
                    },
             'cc': {
                    'command': validus.isemail,
                    'type': 'email address or list of email addresses',
                    },
             'bcc': {
                     'command': validus.isemail,
                     'type': 'email address or list of email addresses',
                     },
            }

    TWILIO = {
              'from_': {
                        'command': validus.isphone,
                        'type': 'phone number',
                        },
              'to': {
                     'command': validus.isphone,
                     'type': 'phone number',
                     },
              'media_url': {
                            'command': validus.isurl,
                            'type': 'url',
                    },
            }

    SLACKWEBHOOK = {
                    'webhook_url': {
                                    'command': validus.isurl,
                                    'type': 'url',
                                    },
                    'attach_urls': {
                                    'command': validus.isurl,
                                    'type': 'url or list of urls',
                                    },
                    }

    def __init__(self):
        pass


    def validate_input(self, msg, attr):
        """
        Validate the given input for correct types, using
        regular expressions with the 'validus' package.  Actual validation
        is done via the is_valid() method so the functools.lru_cache decorator
        can be used to memoize/cache inputs.

        Args:
            :msg: object, any instantiated message class
                i.e. e = Email(*args)
            :attr: str, the attribute to validate

        Returns:
            None, but raises InvalidMessageInputError if Validator._is_valid()
                returns False.

        Usage:
            This is used by the __setattr__ override in the
            _interface.Message class, inherited by message classes.
        """
        msgtype = msg.__class__.__name__.upper()
        inputs = getattr(msg, attr)

        if attr in getattr(Validator, msgtype).keys() and inputs is not None:

            if isinstance(inputs, list):
                for i in inputs:
                    if not self._is_valid(msgtype, attr, i):
                        raise InvalidMessageInputError(msg.__class__.__name__,
                            i, getattr(Validator, msgtype)[attr]['type'])
            else:
                if not self._is_valid(msgtype, attr, inputs):
                    raise InvalidMessageInputError(msg.__class__.__name__,
                            inputs, getattr(Validator, msgtype)[attr]['type'])


    @staticmethod
    @functools.lru_cache(maxsize=256)
    def _is_valid(msgtype, attr, val):
        """
        Check each individual input and cache the result via the
        functools.lru_cache decorator to speed up subsequent calls with
        the same input.

        Args:
            :msgtype: str.upper(), type of message in uppercase format
            :attr:, str, the attribute to validate
            :val:, str, the value of that attribute (attr)

        Returns:
            bool, from operation of `command(val)`.  i.e. True if the
                'val' is valid, False otherwise.

        Example inputs:
            Validator._is_valid('EMAIL', 'from_', 'me@here.com')
            returns True
        """
        msgtype = getattr(Validator, msgtype)
        command = msgtype[attr]['command']
        return command(val)


VALIDATOR = Validator()
