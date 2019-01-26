"""Utility Module - functions useful to other modules."""

import datetime
from collections.abc import MutableSequence

import validus

from ._exceptions import InvalidMessageInputError


"""
Functions below this header are property factories and input validation functions
used by each of the message classes in order to obscure (credentials) or validate
certain attributes.  Each will be defined as a class attribute for each message
(before __init__).
"""


def credential_property(cred):
    """
    A credential property factory for each message class that will set
    private attributes and return obfuscated credentials when requested.
    """

    def getter(instance):
        return "***obfuscated***"

    def setter(instance, value):
        private = "_" + cred
        instance.__dict__[private] = value

    return property(fget=getter, fset=setter)


def validate_property(attr):
    """
    A property factory that will dispatch the to a specific validator function
    that will validate the user's input to ensure critical parameters are of a
    specific type.
    """

    def getter(instance):
        return instance.__dict__[attr]

    def setter(instance, value):
        validate_input(instance.__class__.__name__, attr, value)
        instance.__dict__[attr] = value

    return property(fget=getter, fset=setter)


def validate_input(msg_type, attr, value):
    """Base function to validate input, dispatched via message type."""
    try:
        valid = {
            "Email": validate_email,
            "Twilio": validate_twilio,
            "SlackWebhook": validate_slackwebhook,
            "SlackPost": validate_slackpost,
            "TelegramBot": validate_telegrambot,
            "WhatsApp": validate_whatsapp,
        }[msg_type](attr, value)
    except KeyError:
        return 1
    else:
        return 0


def check_valid(msg_type, attr, value, func, exec_info):
    """
    Checker function all validate_* functions below will call.
    Raises InvalidMessageInputError if input is not valid as per
    given func.
    """
    if value is not None:
        if isinstance(value, MutableSequence):
            for v in value:
                if not func(v):
                    raise InvalidMessageInputError(msg_type, attr, value, exec_info)
        else:
            if not func(value):
                raise InvalidMessageInputError(msg_type, attr, value, exec_info)


def validate_email(attr, value):
    """Email input validator function."""
    check_valid("Email", attr, value, validus.isemail, "email address")


def validate_twilio(attr, value):
    """Twilio input validator function."""
    if attr in ("from_", "to"):
        check_valid("Twilio", attr, value, validus.isphone, "phone number")
    elif attr in ("attachments"):
        check_valid("Twilio", attr, value, validus.isurl, "url")


def validate_slackwebhook(attr, value):
    """SlackWebhook input validator function."""
    check_valid("SlackWebhook", attr, value, validus.isurl, "url")


def validate_slackpost(attr, value):
    """SlackPost input validator function."""
    if attr in ("channel", "credentials"):
        if not isinstance(value, str):
            raise InvalidMessageInputError("SlackPost", attr, value, "string")
    elif attr in ("attachments"):
        check_valid("SlackPost", attr, value, validus.isurl, "url")


def validate_telegrambot(attr, value):
    """TelegramBot input validator function."""
    check_valid("TelegramBot", attr, value, validus.isint, "integer as a string")


def validate_whatsapp(attr, value):
    """WhatsApp input validator function."""
    if attr in ("from_", "to"):
        if value is not None and "whatsapp:" in value:
            value = value.split("whatsapp:+")[-1]
        check_valid(
            "WhatsApp",
            attr,
            value,
            validus.isint,
            "phone number starting with the '+' symbol",
        )
    elif attr in ("attachments"):
        check_valid("WhatsApp", attr, value, validus.isurl, "url")


"""
Functions below this hearder are general utility functions.
"""


def timestamp():
    """Get current date and time."""
    return "{:%Y-%b-%d %H:%M:%S}".format(datetime.datetime.now())
