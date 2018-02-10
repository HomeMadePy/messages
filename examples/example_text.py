import time

import messages
from messages import Twilio


ACCT_SID = 'enter your account sid here'
AUTH_TOKEN = 'enter your auth token here'
TWILIO_NUMBER = 'enter your twilio phone number here'
DESTINATION_NUMBER = 'enter the destination phone number here'


"""Create and send message via messages.send() api."""
kwargs = {'acct_sid': ACCT_SID, 'auth_token': AUTH_TOKEN,
          'from_': TWILIO_NUMBER, 'to': DESTINATION_NUMBER,
          'body': 'Example Message from the API',
          'media_url': 'https://imgs.xkcd.com/comics/python.png'
          }

messages.send('twilio', **kwargs)
#messages.send('twilio', send_async=True, **kwargs)


time.sleep(1)


"""Create Twilio message manually."""
t = Twilio(acct_sid=ACCT_SID, auth_token=AUTH_TOKEN,
           from_=TWILIO_NUMBER, to=DESTINATION_NUMBER,
           body='Example Message!',
           media_url='https://imgs.xkcd.com/comics/python.png')


t.send()
#t.send_async()

print(t.sent_messages)
