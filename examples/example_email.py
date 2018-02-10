import time

import messages
from messages import Email

SERVER = 'specify your email sever here, like smtp.gmail.com'
PORT = 465  # integer - the server port number
PASSWORD = 'put your password here'
FROM = 'put the from email adddress here'
TO = 'put the destination email address here'
CC = None
BCC = None


"""Create and send message via messages.send() api."""
kwargs = {'server_name': SERVER, 'server_port': PORT, 'password': PASSWORD,
          'from_': FROM, 'to': TO, 'cc': CC, 'bcc': BCC,
          'subject': 'Example message from the API', 'body': 'Test message',
          'attachments': None
          }

messages.send('email', **kwargs)
#messages.send('email', send_async=True, **kwargs)


time.sleep(1)


"""Create Email message manually."""
e = Email(server_name=SERVER, server_port=PORT, password=PASSWORD,
          from_=FROM, to=TO, cc=CC, bcc=BCC, subject='Example message',
          body='This is a test!', attachments=None)

e.send()
#e.send_async()

print(e.sent_messages)
