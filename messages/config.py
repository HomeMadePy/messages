"""
Configuration module.

Handles the creation/editing of configuration files and saving of
default attributes, credentials, etc.
"""

from getpass import getpass

import jsonconfig


def configure(msg, params, to_save, credentials):
    """
    Get default values and credentials from a configuration profile.
    If not created, and save=True in the msg class parameter, then
    configuration file is created.

    Args:
        :msg: (Message class) an instance of a message class
        :params: (dict) dict of params passed to message classes' __init__
            method
        :to_save: (set or list) list of default values to save (from address,
            server name, etc.)
        :credentials: (set or list) list of credentials (password, auth_tokens,
            etc.)
    """
    msg_type = msg.__class__.__name__.lower()
    defaults = set(to_save)
    creds = set(credentials)

    with jsonconfig.Config('messages') as cfg:
        if params['profile'] is None:
            msg.profile = 'default_user'
        else:
            msg.profile = params['profile']

        if msg.profile not in cfg.data:
            cfg.data[msg.profile] = {}

        if msg_type not in cfg.data[msg.profile]:
                cfg.data[msg.profile][msg_type] = {}

        for d in defaults:
            setattr(msg, d, cfg.data[msg.profile][msg_type].get(d, params[d]))

        for c in creds:
            setattr(msg, c, (params[c] or cfg.pwd.get(
                msg.profile + '_' + msg_type, None)))
            if getattr(msg, c) is None:
                setattr(msg, c, getpass('\n' + c + ': '))

        if params['save']:
            for d in defaults:
                cfg.data[msg.profile][msg_type][d] = getattr(msg, d)
            for c in creds:
                cfg.pwd[(msg.profile + '_' + msg_type)] = getattr(msg, c)
            cfg.kwargs['dump']['indent'] = 4


def set_default_profile(profile):
    """Sets the default profile to use in the messages config.json file."""
    with jsonconfig.Config('messages') as cfg:
        cfg.data['default'] = profile
        cfg.kwargs['dump']['indent'] = 4

