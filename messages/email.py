"""
Module designed to make creating and sending emails easy.

1. Email class uses the Python 3 standard library MIMEMultipart email
   object to construct the email.
"""

import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication


class Email:
    """
    Create and send emails using the built-in email package.

    Args:
        server_name: str, i.e. 'smtp.gmail.com'
        server_port: int, i.e. 465
        password: str
        From: str, i.e. 'me@here.com'
        To: str or list, i.e. 'you@there.com' or ['a@there.com', 'b@there.com']
        Cc: str or list
        Bcc: str or list
        subject: str
        body_text: str
        attachments: list, i.e. ['/home/you/file1.txt', '/home/you/file2.pdf']

    Usage:
        Create an email object with required Args above.
        Send email with self.send() method.

    Note:
        Some email servers may require you to modify security setting, such as
        gmail allowing "less secure apps" to access the account.  Otherwise
        failure may occur when attempting to send.
    """

    def __init__(self, server_name, server_port, password,
                 from_, to, cc, bcc, subject, body_text, attachments):
        self.server_name = server_name
        self.server_port = server_port
        self.password = password
        self.from_ = from_
        self.to = self.list_to_string(to)
        self.cc = self.list_to_string(cc)
        self.bcc = self.list_to_string(bcc)
        self.subject = subject
        self.body_text = body_text
        self.attachments = attachments
        self.email = 'Email not yet created'


    def __str__(self):
        """print(Email(**args)) method."""
        return('MIMEMultipart Email:'
              '\n\tServer: {}:{}'
              '\n\tFrom: {}'
              '\n\tTo: {}'
              '\n\tCc: {}'
              '\n\tBcc: {}'
              '\n\tSubject: {}'
              '\n\tbody_text: {}...'
              '\n\tattachments: {}'
              .format(self.server_name, self.server_port, self.from_, self.to,
                      self.cc, self.bcc, self.subject, self.body_text[0:40],
                      self.attachments))


    def __repr__(self):
        """repr(Email(**args)) method."""
        return('{}({},{},{},{},{},{},{},{},{},{})'
               .format(self.__class__.__name__, self.server_name,
                       self.server_port, self.password, self.from_,
                       self.to, self.cc, self.bcc, self.subject,
                       self.body_text, self.attachments))


    @staticmethod
    def list_to_string(recipient):
        """
        Format the recipient for the MIMEMultipart() email type.
        If the recipient is a list, then it returns the list as a
        comma separated string.
        """
        if recipient:
            if isinstance(recipient, list):
                return ', '.join(recipient)
            return recipient


    def generate_email(self):
        """Put the parts of the email together."""
        self.email = MIMEMultipart()
        self.add_header()
        self.add_body()
        self.add_attachments()


    def add_header(self):
        """Add email header info."""
        self.email['From'] = self.from_
        self.email['Subject'] = self.subject


    def add_body(self):
        """Add body content of email."""
        if self.body_text:
            body = MIMEText('text', 'plain')
            body.set_payload(self.body_text)
            self.email.attach(body)


    def add_attachments(self):
        """Add required attachments."""
        num_attached = 0
        if self.attachments:
            for item in self.attachments:
                doc = MIMEApplication(open(item, 'rb').read())
                doc.add_header('Content-Disposition', 'attachment',
                               filename=item)
                self.email.attach(doc)
                num_attached += 1
        return num_attached


    def get_session(self):
        """Start session with email server."""
        session = smtplib.SMTP_SSL(self.server_name, self.server_port)
        session.login(self.from_, self.password)
        return session


    def send(self):
        """Send the message."""
        self.generate_email()
        session = self.get_session()

        recipients = []
        if self.to:
            self.email['To'] = self.to
            recipients += self.to.split(', ')
        if self.cc:
            self.email['Cc'] = self.cc
            recipients += self.cc.split(', ')
        if self.bcc:
            self.email['Bcc'] = self.bcc
            recipients += self.bcc.split(', ')

        session.sendmail(self.from_, recipients, self.email.as_string())
        session.quit()
        print('Message sent...'
              '\n\tTo: {}'
              '\n\tCc: {}'
              '\n\tBcc: {}'
              '\n\tAttachments: {}'
              .format(self.to, self.cc, self.bcc, self.attachments))
