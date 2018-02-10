import time

import messages
from messages import SlackWebhook

WEBHOOK_URL = 'put your slack team webhook url here.'


kwargs = {'webhook_url': WEBHOOK_URL, 'body': 'Test message from the API.',
          'attach_urls': 'https://imgs.xkcd.com/comics/python.png',
          'params': {'author_name': 'Mr. Roboto API'}
          }

messages.send('slackwebhook', **kwargs)
#messages.send('slackwebhook', send_async=True, **kwargs)


time.sleep(1)


"""Create SlackWebhook message manually."""
s = SlackWebhook(webhook_url=WEBHOOK_URL, body='This is a Test!',
                 attach_urls='https://imgs.xkcd.com/comics/python.png',
                 params={'author_name': 'Mr. Roboto!'})


s.send()
#s.send_async()

print(s.sent_messages)
