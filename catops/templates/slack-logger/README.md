# Slack Logger Handler

## Features

- Sets up a NoOps endpoint which relays logging messages to Slack

## Setup

### Lambda Setup

1. serverless config credentials --provider aws --key AKIAIOSFODNN7EXAMPLE --secret wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY # add credentials
2. Check [serverless.yml](serverless.yml)
  - Correct service name
  - Correct aws credentials profile
  - Correct http path
3. Set token value in [tokens.yml](tokens.yml) (don't commit these to Git)
4. Run `sls deploy`

### Slack Setup
1. [Create a New Slack App.](https://api.slack.com/apps)
2. Add a Bot User

## Handler Usage

See [](slack_handler.py).

```python
import logging
from slack_handler import SlackHandler

FORMAT = '{\
    "channels":["#channel1", "#channel2"],\
    "time":"%(asctime)s", \
    "level":"%(levelname)s", \
    "message":"%(message)s"}'

logger = logging.getLogger('slack-logger')
logger.setLevel(logging.INFO)
handler = SlackHandler('lambda-url') # Could store this in env variable
handler.setFormatter(logging.Formatter(FORMAT))
logger.addHandler(handler)
logger.INFO('Test slack logging')
```

## Installing [serverless framework](https://serverless.com)

```bash
sudo apt-get install npm
sudo npm install -g serverless
npm install serverless-python-requirements # In this dir
```

