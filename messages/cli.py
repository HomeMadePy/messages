"""command-line interface for messages package."""

import os
import sys

from .exceptions import MessageTypeError
from .exceptions import MESSAGES

import click
from click import option


@click.command()
@click.version_option(version='0.1.2', prog_name='Messages')
@option('-t', '--type', help='Choose message type.')
@option('-f', '--from', help='Specify from email/phone/etc.')
@option('-r', '--recipient', multiple=True,
    help='Specify one or more primary (TO) recipients.')
@option('-c', '--carboncopy', multiple=True,
    help='Specify one or more carbon copy (CC) addresses.')
@option('-b', '--blindcopy', multiple=True,
    help='Specify one or more blind carbon copy (BCC) addresses.')
@option('-s', '--subject', help='Message subject line.')
@option('-m', '--message', help='Message body -- text or filepath.')
@option('-a', '--attach', multiple=True,
    help='Specify one or more filepaths or urls to attach.')
@click.pass_context
def main(ctx, **kwds):
    """Specify Type, Recipients, and Content to send."""
    print(kwds)

    if not any([val for key, val in kwds.items()]):
        click.echo(ctx.get_usage())
        click.echo('Try messages --help for more information.')
        sys.exit(0)

    if kwds['type'].lower() not in MESSAGES:
        raise MessageTypeError(kwds['type'])

    if kwds['message']:
        if os.path.isfile(kwds['message']):
            message = open(kwds['message'], 'r').read()

