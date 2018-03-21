"""command-line interface for messages package."""

import os
import sys

import click
from click import argument
from click import option


from messages import MESSAGES
from .api import send
from .exceptions import UnsupportedMessageTypeError


def check_args(ctx, kwds):
    """If no CLI args given, prints usage and exits."""
    if not any([val for key, val in kwds.items()]):
        click.echo(ctx.get_usage())
        click.echo('Try messages --help for more information.')
        sys.exit(0)


def check_type(kwds):
    """If no or incorrect message-type specified, alerts user and exits."""
    if not kwds['type']:
        click.echo('[!] Must specify message type with -t option.')
        click.echo('Try messages --help for more information.')
        sys.exit(0)
    if kwds['type'].lower() not in MESSAGES:
        raise UnsupportedMessageTypeError(kwds['type'])


def get_body(kwds):
    """Reads message body if specified via filepath."""
    if kwds['file'] and os.path.isfile(kwds['file']):
        kwds['body'] = open(kwds['file'], 'r').read()
        kwds['file'] = None


def trim_args(kwds):
    """Gets rid of args with value of None, as well as select keys."""
    reject_key = ('type')
    reject_val = (None, ())
    kwargs = {k:v for k,v in kwds.items() if k not in ('type') and
                                             v not in (None, ())}
    for k, v in kwargs.items():
        if k in ('to', 'cc', 'bcc', 'attach'):
            kwargs[k] = list(kwargs[k])
    return kwargs


@click.command()
@argument('type', required=True)
@option('-f', '--from_',
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
@option('-a', '--attach', multiple=True,
    help='Attachments -- filepath or url to attach.')
@option('-S', '--save', is_flag=True,
    help='Save default values/credentials.')
@option('-P', '--profile',
    help='Specify pre-configured user profile.')
@option('-T', '--types',
    help='List available message types.')
@click.version_option(version='0.3.1', prog_name='Messages')
@click.pass_context
def main(ctx, **kwds):
    """Specify Message-Type, Recipients, and Content to send."""

    check_args(ctx, kwds)
    check_type(kwds)
    get_body(kwds)
    kwargs = trim_args(kwds)

    send(kwds['type'], send_async=True, **kwargs)
