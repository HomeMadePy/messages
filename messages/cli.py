"""command-line interface for messages package."""

import os

import click
from click import option

from messages import __version__ as VERSION
from .api import send
from ._config import create_config_profile
from ._config import CONFIG


##############################################################################
# Utility functions
##############################################################################


def get_body_from_file(kwds):
    """Reads message body if specified via filepath."""
    if kwds["file"] and os.path.isfile(kwds["file"]):
        kwds["body"] = open(kwds["file"], "r").read()
        kwds["file"] = None


def trim_args(kwds):
    """Gets rid of args with value of None, as well as select keys."""
    reject_key = ("type", "types", "configure")
    reject_val = (None, ())
    kwargs = {
        k: v for k, v in kwds.items() if k not in reject_key and v not in reject_val
    }
    for k, v in kwargs.items():
        if k in ("to", "cc", "bcc", "attachments"):
            kwargs[k] = list(kwargs[k])
    return kwargs


def send_message(msg_type, kwds):
    """Do some final preprocessing and send the message."""
    if kwds["file"]:
        get_body_from_file(kwds)
    kwargs = trim_args(kwds)
    send(msg_type, send_async=True, **kwargs)


##############################################################################
# Command Line Interface functions
##############################################################################


@click.group()
@click.version_option(version=VERSION, prog_name="Messages")
def main():
    """See available commands below to create appropriate message."""
    pass


@main.command("configure")
@click.argument("msg_type", required=True)
def main_configure(msg_type):
    """Configure profiles for the given message type."""
    create_config_profile(msg_type)


@main.command("email")
@click.argument("profile", type=click.STRING, required=False)
@click.argument("body", type=click.STRING, default="", required=False)
@option("-f", "--from", "from_", help="Originating (from) email address")
@option("-t", "--to", multiple=True, help="Recipient email addresses.")
@option(
    "-c", "--carboncopy", "cc", multiple=True, help="Carbon Copy (CC) email addresses."
)
@option(
    "-b",
    "--blindcopy",
    "bcc",
    multiple=True,
    help="Blind Carbon Copy (BCC) email addresses.",
)
@option("-s", "--subject", help="Subject line.")
@option("-m", "--file", help="Read message body from filepath.")
@option(
    "-a",
    "--attach",
    "attachments",
    multiple=True,
    help="Attachments -- filepath to attach.",
)
@option("-S", "--save", is_flag=True, help="Save default values in current profile.")
@option(
    "-V",
    "--verbose",
    is_flag=True,
    help="Display verbose output and debug information.",
)
@click.pass_context
def main_email(ctx, **kwds):
    """Send email message.

    * [PROFILE]: Pre-configured user profile.

    * [BODY]:    Message body text.

    * Example: messages email myEmailProfile 'Hello from email.' -t 'first@test.com' -c 'second@test.com' -s 'TestSubject'
    --attach ./sample.txt --verbose
    """
    send_message("email", kwds)


@main.command("twilio")
@click.argument("profile", type=click.STRING, required=False)
@click.argument("body", type=click.STRING, default="", required=False)
@option("-f", "--from", "from_", help="Originating (from) phone number.")
@option("-t", "--to", multiple=True, help="Recipient phone number.")
@option("-m", "--file", help="Read message body from filepath.")
@option(
    "-a",
    "--attach",
    "attachments",
    multiple=True,
    help="Attachments -- url for image to attach.",
)
@option("-S", "--save", is_flag=True, help="Save default values in current profile.")
@option(
    "-V",
    "--verbose",
    is_flag=True,
    help="Display verbose output and debug information.",
)
@click.pass_context
def main_twilio(ctx, **kwds):
    """Send twilio text message.

    * [PROFILE]: Pre-configured user profile.

    * [BODY]:    Message body text.

    * Example: messages twilio myTwilioProfile 'hello from twilio' -t '+12223334444' --verbose
    """
    send_message("twilio", kwds)


@main.command("slackwebhook")
@click.argument("profile", type=click.STRING, required=False)
@click.argument("body", type=click.STRING, default="", required=False)
@option("-m", "--file", help="Read message body from filepath.")
@option(
    "-a",
    "--attach",
    "attachments",
    multiple=True,
    help="Attachments -- url for image to attach.",
)
@option("-S", "--save", is_flag=True, help="Save default values in current profile.")
@option(
    "-V",
    "--verbose",
    is_flag=True,
    help="Display verbose output and debug information.",
)
@click.pass_context
def main_slackwebhook(ctx, **kwds):
    """Send SlackWebhook message.

    * [PROFILE]: Pre-configured user profile.

    * [BODY]:    Message body text.

    * Example: messages slackwebhook mySlackWebhookProfile "Hello from slackwebhook." -a "https://somewebresource.jpg" --verbose
    """
    send_message("slackwebhook", kwds)


@main.command("slackpost")
@click.argument("profile", type=click.STRING, required=False)
@click.argument("body", type=click.STRING, default="", required=False)
@option("-c", "--channel", help="Slack channel to post message to.")
@option("-m", "--file", help="Read message body from filepath.")
@option(
    "-a",
    "--attach",
    "attachments",
    multiple=True,
    help="Attachments -- url for image to attach.",
)
@option("-S", "--save", is_flag=True, help="Save default values in current profile.")
@option(
    "-V",
    "--verbose",
    is_flag=True,
    help="Display verbose output and debug information.",
)
@click.pass_context
def main_slackpost(ctx, **kwds):
    """Send SlackPost message.

    * [PROFILE]: Pre-configured user profile.

    * [BODY]:    Message body text.

    * Example: mesages slackpost mySlackProfile "Hello from Slack." -c "#general" --verbose
    """
    send_message("slackpost", kwds)


@main.command("telegram")
@click.argument("profile", type=click.STRING, required=False)
@click.argument("body", type=click.STRING, default="", required=False)
@option("-c", "--chat-id", help="Chat ID to send message to.")
@option("-m", "--file", help="Read message body from filepath.")
@option(
    "-a",
    "--attach",
    "attachments",
    multiple=True,
    help="Attachments -- url for image to attach.",
)
@option("-S", "--save", is_flag=True, help="Save default values in current profile.")
@option(
    "-V",
    "--verbose",
    is_flag=True,
    help="Display verbose output and debug information.",
)
@click.pass_context
def main_telegram(ctx, **kwds):
    """Send TelegramBot message.

    * [PROFILE]: Pre-configured user profile.

    * [BODY]:    Message body text.

    * Example: messages telegram myTelegramProfile "Hello from Telegram." -a "https://somefile.jpg" --verbose
    """
    send_message("telegrambot", kwds)


@main.command("whatsapp")
@click.argument("profile", type=click.STRING, required=False)
@click.argument("body", type=click.STRING, default="", required=False)
@option("-f", "--from", "from_", help="Originating (from) phone number.")
@option("-t", "--to", multiple=True, help="Recipient phone number.")
@option("-m", "--file", help="Read message body from filepath.")
@option(
    "-a",
    "--attach",
    "attachments",
    multiple=True,
    help="Attachments -- url for image to attach.",
)
@option("-S", "--save", is_flag=True, help="Save default values in current profile.")
@option(
    "-V",
    "--verbose",
    is_flag=True,
    help="Display verbose output and debug information.",
)
@click.pass_context
def main_whatsapp(ctx, **kwds):
    """Send WhatsApp text message via the Twilio API.

    * [PROFILE]: Pre-configured user profile.

    * [BODY]:    Message body text.

    * Example: messages whatsapp myWhatsAppProfile 'hello from whatsapp' -t '+12223334444' --verbose
    """
    send_message("whatsapp", kwds)
