"""Utility Module - functions useful to other modules."""

import validus

from .exceptions import InvalidMessageInputError


"""
Functions below this header are used within the _interface.py module in
order to validate user-input to specific fields.
"""

def validate_input(msg, attr, valid=True):
    """Base function to validate input, dispatched via message type."""
    try:
        valid = {
            'Email': validate_email,
            'Twilio': validate_twilio,
            'SlackWebhook': validate_slackwebhook,
        }[msg.__class__.__name__](msg, attr)
    except KeyError:
        pass


def check_valid(msg, attr, func, exec_info):
    """
    Checker function all validate_* functions below will call.
    Raises InvalidMessageInputError if input is not valid as per
    given func.
    """
    if getattr(msg, attr) is not None:
        if isinstance(getattr(msg, attr), list):
                for item in getattr(msg, attr):
                        if not func(item):
                            raise InvalidMessageInputError(msg.__class__.__name__,
                                attr, exec_info)

        else:
            if not func(getattr(msg, attr)):
                raise InvalidMessageInputError(msg.__class__.__name__,
                    attr, exec_info)


def validate_email(msg, attr):
    """Email input validator function."""
    if attr in ('from_', 'to', 'cc', 'bcc'):
        check_valid(msg, attr, validus.isemail, 'email address')


def validate_twilio(msg, attr):
    """Twilio input validator function."""
    if attr in ('from_', 'to'):
        check_valid(msg, attr, validus.isphone, 'phone number')
    elif attr in ('media_url'):
        check_valid(msg, attr, validus.isurl, 'url')


def validate_slackwebhook(msg, attr):
    """SlackWebhook input validator function."""
    if attr in ('webhook_url', 'attachments'):
        check_valid(msg, attr, validus.isurl, 'url')
