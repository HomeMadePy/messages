"""
Module designed to make creating and sending emails easy.

1.  Email
    - Uses the Python 3 standard library MIMEMultipart email
      object to construct the email.
"""

import reprlib
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

from ._config import check_config_file
from ._eventloop import MESSAGELOOP
from ._interface import Message
from ._utils import credential_property
from ._utils import validate_property
from ._utils import timestamp


SMTP_SERVERS = {
    "gmail.com": ("smtp.gmail.com", 465),
    "yahoo.com": ("smtp.yahoo.com", 465),
    "yahoo.co.uk": ("smtp.mail.yahoo.co.uk", 465),
    "yahoo.com.au": ("smtp.mail.yahoo.com.au", 465),
    "live.com": ("smtp.live.com", 465),
    "office365.com": ("smtp.office365.com", 587),
    "att.net": ("smtp.att.yahoo.com", 465),
    "verizon.net": ("outgoing.verizon.net", 465),
    "ntlworld.com": ("smtp.ntlworld.com", 465),
    "hotmail.com": ("smtp.live.com", 465),
    "mail.com": ("smtp.mail.com", 465),
}


class Email(Message):
    """
    Create and send emails using the built-in email package.

    Args:
        :from_: (str) originating email address
            i.e. 'me@here.com'
        :to: (str or list) primary message recipients
             i.e. 'you@there.com' or
                  ['her@there.com', 'him@there.com']
        :server: (str) url of smtp server
            i.e. 'smtp.gmail.com'
        :port: (int) smtp server port
            i.e. 465 or 587
        :auth: (str) password for email account
        :cc: (str or list) carbon-copy recipients
        :bcc: (str or list) blind carbon-copy recipients
        :subject: (str) email message subject line
        :body: (str) body text of the message to send
        :attachments: (str or list) files to attach
            i.e. './file1', or
                ['/home/you/file1.txt', '/home/you/file2.pdf']
        :profile: (str) use an account profile specified by name
        :save: (bool) save pertinent values in the messages config.json file,
            such as from_, server, port, auth (encrypted keyring) to make
            sending messages faster.

    Attributes:
        :message: (MIMEMultipart) current form of the message to be constructed

    Managed Attributes (Properties):
        :auth: auth will set as a private attribute (_auth) and obscured when requested
        :from_: user input will validate a proper email address
        :to: user input will be validated for a proper email address
        :cc: user input will be validated for a proper email address
        :bcc: user input will be validated for a proper email address

    Usage:
        Create an email object with required Args above.
        Send email with self.send() or self.send_async() methods.

    Note:
        Some email servers may require you to modify security setting, such as
        gmail allowing "less secure apps" to access the account.  Otherwise
        failure may occur when attempting to send.
    """

    auth = credential_property("auth")
    from_ = validate_property("from_")
    to = validate_property("to")
    cc = validate_property("cc")
    bcc = validate_property("bcc")

    def __init__(
        self,
        from_=None,
        to=None,
        server=None,
        port=None,
        auth=None,
        cc=None,
        bcc=None,
        subject="",
        body="",
        attachments=None,
        profile=None,
        save=False,
        verbose=False,
    ):

        self.from_, self.to, self.cc, self.bcc = from_, to, cc, bcc
        self.server = server or self.get_server(from_)[0]
        self.port = port or self.get_server(from_)[1]
        self.auth = auth
        self.subject = subject
        self.body = body
        self.attachments = attachments or []
        self.profile = profile
        self.save = save
        self.verbose = verbose
        self.message = None

        if self.profile:
            check_config_file(self)

    def __str__(self, indentation="\n"):
        """print(Email(**args)) method.
           Indentation value can be overridden in the function call.
           The default is new line"""
        return (
            "{}Server: {}:{}"
            "{}From: {}"
            "{}To: {}"
            "{}Cc: {}"
            "{}Bcc: {}"
            "{}Subject: {}"
            "{}Body: {}"
            "{}Attachments: {}".format(
                indentation,
                self.server,
                self.port,
                indentation,
                self.from_,
                indentation,
                self.to,
                indentation,
                self.cc,
                indentation,
                self.bcc,
                indentation,
                self.subject,
                indentation,
                reprlib.repr(self.body),
                indentation,
                self.attachments,
            )
        )

    @staticmethod
    def get_server(address=None):
        """Return an SMTP servername guess from outgoing email address."""
        if address:
            domain = address.split("@")[1]
            try:
                return SMTP_SERVERS[domain]
            except KeyError:
                return ("smtp." + domain, 465)
        return (None, None)

    @staticmethod
    def list_to_string(recipient):
        """
        Format the recipient for the MIMEMultipart() email type.
        If the recipient is a list, then it returns the list as a
        comma separated string.
        example: input=['you@here.com', 'her@there.com']
                 output='you@there.com, her@there.com'
        """
        if recipient:
            if isinstance(recipient, list):
                return ", ".join(recipient)
            return recipient

    def _generate_email(self):
        """Put the parts of the email together."""
        self.message = MIMEMultipart()
        self._add_header()
        self._add_body()
        self._add_attachments()

    def _add_header(self):
        """Add email header info."""
        self.message["From"] = self.from_
        self.message["Subject"] = self.subject

    def _add_body(self):
        """Add body content of email."""
        if self.body:
            b = MIMEText("text", "plain")
            b.set_payload(self.body)
            self.message.attach(b)

    def _add_attachments(self):
        """Add required attachments."""
        num_attached = 0
        if self.attachments:
            if isinstance(self.attachments, str):
                self.attachments = [self.attachments]

            for item in self.attachments:
                doc = MIMEApplication(open(item, "rb").read())
                doc.add_header("Content-Disposition", "attachment", filename=item)
                self.message.attach(doc)
                num_attached += 1
        return num_attached

    def _get_session(self):
        """Start session with email server."""
        if self.port in (465, "465"):
            session = self._get_ssl()
        elif self.port in (587, "587"):
            session = self._get_tls()
        session.login(self.from_, self._auth)
        return session

    def _get_ssl(self):
        """Get an SMTP session with SSL."""
        return smtplib.SMTP_SSL(self.server, self.port)

    def _get_tls(self):
        """Get an SMTP session with TLS."""
        session = smtplib.SMTP(self.server, self.port)
        session.ehlo()
        session.starttls()
        session.ehlo()
        return session

    def send(self):
        """Send the message."""
        self._generate_email()

        if self.verbose:
            print(
                "Debugging info"
                "\n--------------"
                "\n{} Message created.".format(timestamp())
            )

        session = self._get_session()
        if self.verbose:
            print(timestamp(), "Login successful.")

        recipients = []
        if self.to:
            self.message["To"] = self.list_to_string(self.to)
            recipients.append(self.to)
        if self.cc:
            self.message["Cc"] = self.list_to_string(self.cc)
            recipients.append(self.cc)
        if self.bcc:
            self.message["Bcc"] = self.list_to_string(self.bcc)
            recipients.append(self.bcc)

        session.sendmail(self.from_, recipients, self.message.as_string())
        session.quit()

        if self.verbose:
            print(timestamp(), "Logged out.")

        if self.verbose:
            print(
                timestamp(),
                type(self).__name__ + " info:",
                self.__str__(indentation="\n * "),
            )

        print("Message sent.")

    def send_async(self):
        """Send message asynchronously."""
        MESSAGELOOP.add_message(self)
