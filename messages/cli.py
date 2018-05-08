"""command-line interface for messages package."""

import os
import sys

import click
from click import argument
from click import option


from messages import MESSAGES
from .api import send
from .config import create_config
from .exceptions import UnsupportedMessageTypeError


def check_args(ctx, kwds):
    """If no CLI args given, prints usage and exits."""
    if not any([val for key, val in kwds.items()]):
        click.echo(ctx.get_usage())
        click.echo('Try messages --help for more information.')
        sys.exit(0)


def check_type(kwds):
    """If incorrect message-type specified, raise error."""
    if kwds['type'].lower() not in MESSAGES.keys():
        raise UnsupportedMessageTypeError(kwds['type'])


def get_body_from_file(kwds):
    """Reads message body if specified via filepath."""
    if kwds['file'] and os.path.isfile(kwds['file']):
        kwds['body'] = open(kwds['file'], 'r').read()
        kwds['file'] = None


def trim_args(kwds):
    """Gets rid of args with value of None, as well as select keys."""
    reject_key = ('type', 'types', 'configure')
    reject_val = (None, ())
    kwargs = {k:v for k,v in kwds.items() if k not in reject_key and
                                             v not in reject_val}
    for k, v in kwargs.items():
        if k in ('to', 'cc', 'bcc', 'attach'):
            kwargs[k] = list(kwargs[k])
    return kwargs


def create_config_entry(msg_type):
    """Creates an entry in the config.json file for later use."""
    print('You will need the following information to configure: ' + msg_type)
    for item in (MESSAGES[msg_type]['defaults'] +
                 MESSAGES[msg_type]['credentials']):
        click.echo('\t* ' + item)

    status = input('\nContinue [Y/N]? ')
    if status in ('Y', 'y'):
        profile = input('\nEnter Profile Name: ')
        create_config(msg_type, profile, MESSAGES[msg_type])


def list_types():
    """Prints all available message types."""
    print('Available messages types:')
    for m in MESSAGES:
        click.echo('\t* ' + m)


@click.command()
@argument('type', required=False)
@option('-f', '--from', 'from_',
    help='From address/phone/etc.')
@option('-t', '--to', multiple=True,
    help='Primary (To) recipient.')
@option('-c', '--carboncopy', multiple=True,
    help='Carbon Copy (CC) addresses.')
@option('-b', '--blindcopy', multiple=True,
    help='Blind Carbon Copy (BCC) addresses.')
@option('-s', '--subject',
    help='Subject line.')
@option('-m', '--body',
    help='Message body text.')
@option('-M', '--file',
    help='Read message body from filepath.')
@option('-a', '--attach', 'attachments', multiple=True,
    help='Attachments -- filepath or url to attach.')
@option('-S', '--save', is_flag=True,
    help='Save default values/credentials.')
@option('-P', '--profile',
    help='Specify pre-configured user profile.')
@option('-T', '--types', is_flag=True,
    help='List available message types and exit.')
@option('-C', '--configure', is_flag=True,
    help='Configure specified message type and exit.')
@click.version_option(version='0.3.3', prog_name='Messages')
@click.pass_context
def main(ctx, **kwds):
    """
    Specify Message-Type, Recipients, and Content to send.

    [TYPE] = email, twilio, ...\n
        try `messages --types` to see all available types
    """

    check_args(ctx, kwds)

    if kwds['type']:
        check_type(kwds)

    if kwds['types']:
        list_types()
        sys.exit(0)

    if kwds['configure']:
        create_config_entry(kwds['type'])
        sys.exit(0)

    if kwds['file']:
        get_body_from_file(kwds)

    kwargs = trim_args(kwds)

    if kwds['type']:
        send(kwds['type'], send_async=True, **kwargs)
    else:
        click.echo('[!] Specify message type')
        list_types()
        click.echo('Try `messages --help` for more information')
        sys.exit(0)

