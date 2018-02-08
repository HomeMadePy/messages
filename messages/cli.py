"""command-line interface for messages package."""

import os
import sys

import click
from click import option

from .exceptions import MessageTypeError
from .exceptions import MESSAGES
from .email_ import Email
from .text import Twilio
from .slack import SlackWebhook


def _message_factory(**args):
    """
    Factory function that creates the desired message type with the
    given **args as arguments.
    """
    if args['type'].lower() == 'email':
        return Email(server_name=args['credentials'][0],
                server_port=int(args['credentials'][1]),
                password=args['credentials'][2],
                from_=args['from'],
                to=list(args['recipient']) or None,
                cc=list(args['carboncopy']) or None,
                bcc=list(args['blindcopy']) or None,
                subject=args['subject'],
                body=args['body'],
                attachments=list(args['attach']) or None)






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
@option('-X', '--credentials', multiple=True,
    help='Credentials for given service.')
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

    msg = _message_factory(**kwds)
    print(msg)      #just for debugging
    #msg.send_async()
