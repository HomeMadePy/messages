"""command-line interface for messages package."""

import os
import sys

import click
from click import option

from messages import MESSAGES
from .api import send
from .exceptions import MessageTypeError
from .email_ import Email
from .text import Twilio
from .slack import SlackWebhook



@click.command()
@option('-t', '--type',
    help='Choose message type.')
@option('-f', '--from',
    help='Specify from email/phone/etc.')
@option('-r', '--recipient', multiple=True,
    help='Specify one or more primary (To) recipients.')
@option('-c', '--carboncopy', multiple=True,
    help='Specify one or more carbon copy (CC) addresses.')
@option('-b', '--blindcopy', multiple=True,
    help='Specify one or more blind carbon copy (BCC) addresses.')
@option('-s', '--subject',
    help='Message subject line.')
@option('-m', '--body',
    help='Message body -- text or filepath.')
@option('-a', '--attach', multiple=True,
    help='Specify one or more filepaths or urls to attach.')
@option('-C', '--configure',
    help='Configure and preset default values.')
@option('-U', '--user',
    help='Specify pre-configured user account name.')
@click.version_option(version='0.1.2', prog_name='Messages')
@click.pass_context
def main(ctx, **kwds):
    """Specify Type, Recipients, and Content to send."""

    print(kwds)     #just for debugging

    if not any([val for key, val in kwds.items()]):
        click.echo(ctx.get_usage())
        click.echo('Try messages --help for more information.')
        sys.exit(0)

    if not kwds['type']:
        click.echo('** Must specify message type with -t option.')
        click.echo('Try messages --help for more information.')
        sys.exit(0)

    if kwds['configure']:
        #call configuration functions
        #can be used in tandem with sending an actual message
        #just save all the values given; like credentials, from-address, etc.
        pass

    if kwds['type'].lower() not in MESSAGES:
        raise MessageTypeError(kwds['type'])

    if kwds['body']:
        if os.path.isfile(kwds['body']):
            message = open(kwds['body'], 'r').read()


