"""
Module designed to make creating and sending WhatsApp messages easy.

1.  WhatsApp
    - Uses the Twilio API to send WhatsApp messages, thus inherits from the
      Twilio class.
    - Must have an account_sid, auth_token, and a twilio phone number
      in order to use.
    - Go to https://www.twilio.com/whatsapp to register.
"""

from ._config import check_config_file
from ._utils import credential_property
from ._utils import validate_property
from .text import Twilio


class WhatsApp(Twilio):
    """
    Create and send WhatsApp messages using the WhatsApp API provided by
    Twilio.

    Inheritance:
        :Twilio: Inherits functionality from Twilio class.  See the
            messages.text.Twilio class.

    Args:
        :from_: (str) phone number of originating text, e.g. '+15558675309'
        :to: (str) phone number of destination text, e.g. '+15558675309'
        :auth: (list or tuple) twilio api credentials: (acct_sid, auth_token)
        :body: (str) message to send
        :attachments: (str) url of any image to send along with message
        :profile: (str) use a separate account profile specified by name
        :save: (bool) save pertinent values in the messages config file,
            such as from_, acct_sid, auth_token (encrypted keyring) to make
            sending messages faster.

    Attributes:
        :sid: (str) return value from send, record of sent message

    Managed Attributes (Properties):
        :auth: auth will set as a private attribute (_auth) and obscured when requested
        :from_: user input will be validated for a proper phone number
        :to: user input will be validated for a proper phone number
        :attachments: user input will be validated for a proper url

    Usage:
        Create a WhatsApp message instance with required Args above.
        Send message with self.send() or self.send_async() methods.

    Notes:
        For API description:
        https://www.twilio.com/docs/sms/whatsapp/quickstart
    """

    auth = credential_property("auth")
    from_ = validate_property("from_")
    to = validate_property("to")
    attachments = validate_property("attachments")

    def __init__(
        self,
        from_=None,
        to=None,
        auth=None,
        body="",
        attachments=None,
        profile=None,
        save=False,
        verbose=False,
    ):

        self.from_ = "whatsapp:" + from_
        self.to = "whatsapp:" + to
        self.auth = auth
        self.body = body
        self.attachments = attachments
        self.profile = profile
        self.save = save
        self.verbose = verbose
        self.sid = None

        if self.profile:
            check_config_file(self)
