"""
Configuration module.

Handles the creation/editing of configuration files and saving of
default attributes, credentials (auth), etc.
"""

from collections import MutableSequence
from collections import OrderedDict
from getpass import getpass

import jsonconfig

from ._exceptions import UnknownProfileError


##############################################################################
#  Message class config defaults
##############################################################################

CONFIG = {
    "email": {
        "settings": {
            "from_": "From email address (e.g. you@here.com)",
            "server": "Email server url (e.g. smtp.here.com)",
            "port": "Email server port number (e.g. 465)",
        },
        "auth": {"auth": "Email service password"},
    },
    "slackwebhook": {
        "settings": {"from_": "Name or alias of sender (optional)"},
        "auth": {"auth": "Slack API Webhook URL"},
    },
    "slackpost": {
        "settings": {
            "from_": "Name or alias of sender (optional)",
            "channel": "Channel to post message to (e.g. #general)",
        },
        "auth": {"auth": "Slack API authentication token"},
    },
    "twilio": {
        "settings": {"from_": "Twilio phone number (e.g. +19998675309)"},
        "auth": OrderedDict(
            [
                ("auth_sid", "Twilio API account SID"),
                ("auth_token", "Twilio API authorization token"),
            ]
        ),
    },
    "telegrambot": {
        "settings": {"channel_id": "Telegram Channel ID of chat"},
        "auth": {"auth": "Telegram authorization token"},
    },
    "whatsapp": {
        "settings": {"from_": "Twilio phone number (e.g. +19998675309)"},
        "auth": OrderedDict(
            [
                ("auth_sid", "Twilio API account SID"),
                ("auth_token", "Twilio API authorization token"),
            ]
        ),
    },
}


##############################################################################
#  Config functions used by Message classes
##############################################################################


def check_config_file(msg):
    """
    Checks the config.json file for default settings and auth values.

    Args:
        :msg: (Message class) an instance of a message class.
    """
    with jsonconfig.Config("messages", indent=4) as cfg:
        verify_profile_name(msg, cfg)

        retrieve_data_from_config(msg, cfg)

        if msg._auth is None:
            retrieve_pwd_from_config(msg, cfg)

        if msg.save:
            update_config_data(msg, cfg)
            update_config_pwd(msg, cfg)


def verify_profile_name(msg, cfg):
    """
    Verifies the profile name exists in the config.json file.

    Args:
        :msg: (Message class) an instance of a message class.
        :cfg: (jsonconfig.Config) config instance.
    """
    if msg.profile not in cfg.data:
        raise UnknownProfileError(msg.profile)


def retrieve_data_from_config(msg, cfg):
    """
    Update msg attrs with values from the profile configuration if the
    msg.attr=None, else leave it alone.

    Args:
        :msg: (Message class) an instance of a message class.
        :cfg: (jsonconfig.Config) config instance.
    """
    msg_type = msg.__class__.__name__.lower()
    for attr in msg:
        if getattr(msg, attr) is None and attr in cfg.data[msg.profile][msg_type]:
            setattr(msg, attr, cfg.data[msg.profile][msg_type][attr])


def retrieve_pwd_from_config(msg, cfg):
    """
    Retrieve auth from profile configuration and set in msg.auth attr.

    Args:
        :msg: (Message class) an instance of a message class.
        :cfg: (jsonconfig.Config) config instance.
    """
    msg_type = msg.__class__.__name__.lower()
    key_fmt = msg.profile + "_" + msg_type
    pwd = cfg.pwd[key_fmt].split(" :: ")
    if len(pwd) == 1:
        msg.auth = pwd[0]
    else:
        msg.auth = tuple(pwd)


def update_config_data(msg, cfg):
    """
    Updates the profile's config entry with values set in each attr by the
    user.  This will overwrite existing values.

    Args:
        :msg: (Message class) an instance of a message class.
        :cfg: (jsonconfig.Config) config instance.
    """
    for attr in msg:
        if attr in cfg.data[msg.profile] and attr is not "auth":
            cfg.data[msg.profile][attr] = getattr(msg, attr)


def update_config_pwd(msg, cfg):
    """
    Updates the profile's auth entry with values set by the user.
    This will overwrite existing values.

    Args:
        :msg: (Message class) an instance of a message class.
        :cfg: (jsonconfig.Config) config instance.
    """
    msg_type = msg.__class__.__name__.lower()
    key_fmt = msg.profile + "_" + msg_type
    if isinstance(msg._auth, (MutableSequence, tuple)):
        cfg.pwd[key_fmt] = " :: ".join(msg._auth)
    else:
        cfg.pwd[key_fmt] = msg._auth


##############################################################################
#  Config functions used by the CLI to create profile entries
##############################################################################


def create_config_profile(msg_type):
    """
    Create a profile for the given message type.

    Args:
        :msg_type: (str) message type to create config entry.
    """
    msg_type = msg_type.lower()

    display_required_items(msg_type)

    if get_user_ack():
        profile_name = input("Profile Name: ")
        data = get_data_from_user(msg_type)
        auth = get_auth_from_user(msg_type)
        configure_profile(msg_type, profile_name, data, auth)


def display_required_items(msg_type):
    """
    Display the required items needed to configure a profile for the given
    message type.

    Args:
        :msg_type: (str) message type to create config entry.
    """
    print("Configure a profile for: " + msg_type)
    print("You will need the following information:")
    for k, v in CONFIG[msg_type]["settings"].items():
        print("   * " + v)
    print("Authorization/credentials required:")
    for k, v in CONFIG[msg_type]["auth"].items():
        print("   * " + v)


def get_user_ack():
    """
    Get the user's acknowledgement to continue.

    Returns: bool
    """
    ack = input("\nContinue [Y/N]? ")
    return ack in ("y", "Y")


def get_data_from_user(msg_type):
    """Get the required 'settings' from the user and return as a dict."""
    data = {}
    for k, v in CONFIG[msg_type]["settings"].items():
        data[k] = input(v + ": ")
    return data


def get_auth_from_user(msg_type):
    """Get the required 'auth' from the user and return as a dict."""
    auth = []
    for k, v in CONFIG[msg_type]["auth"].items():
        auth.append((k, getpass(v + ": ")))
    return OrderedDict(auth)


def configure_profile(msg_type, profile_name, data, auth):
    """
    Create the profile entry.

    Args:
        :msg_type: (str) message type to create config entry.
        :profile_name: (str) name of the profile entry
        :data: (dict) dict values for the 'settings'
        :auth: (dict) auth parameters
    """
    with jsonconfig.Config("messages", indent=4) as cfg:
        write_data(msg_type, profile_name, data, cfg)
        write_auth(msg_type, profile_name, auth, cfg)

    print("[+] Configuration entry for <" + profile_name + "> created.")
    print("[+] Configuration file location: " + cfg.filename)


def write_data(msg_type, profile_name, data, cfg):
    """
    Write the settings into the data portion of the cfg.

    Args:
        :msg_type: (str) message type to create config entry.
        :profile_name: (str) name of the profile entry
        :data: (dict) dict values for the 'settings'
        :cfg: (jsonconfig.Config) config instance.
    """
    if profile_name not in cfg.data:
        cfg.data[profile_name] = {}
    cfg.data[profile_name][msg_type] = data


def write_auth(msg_type, profile_name, auth, cfg):
    """
    Write the settings into the auth portion of the cfg.

    Args:
        :msg_type: (str) message type to create config entry.
        :profile_name: (str) name of the profile entry
        :auth: (dict) auth parameters
        :cfg: (jsonconfig.Config) config instance.
    """
    key_fmt = profile_name + "_" + msg_type
    pwd = []
    for k, v in CONFIG[msg_type]["auth"].items():
        pwd.append(auth[k])

    if len(pwd) > 1:
        cfg.pwd[key_fmt] = " :: ".join(pwd)
    else:
        cfg.pwd[key_fmt] = pwd[0]
