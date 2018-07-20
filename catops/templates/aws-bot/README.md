# Serverless Slack Bot

## Features

- Responds to @mentions of your Slack bot.
- Can use the Slack API.

## Setup

### Lambda Setup

1. serverless config credentials --provider aws --key AKIAIOSFODNN7EXAMPLE --secret wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY # add credentials
2. Check [serverless.yml](serverless.yml)
  - Correct service name
  - Correct aws credentials profile
  - Correct http path
3. Set token value in [tokens.yml](tokens.yml) (don't commit these to Git)
4. Run `sls deploy`

### Slack setup
1. [Create a New Slack App.](https://api.slack.com/apps)
2. Add a Bot User
3. Event Subscriptions -> Enable Events
  - Enter the Request URL after running `sls deploy` and using the POST url
  - Add Bot User Event `app_mention`

## Installing [serverless framework](https://serverless.com)

```bash
sudo apt-get install npm
sudo npm install -g serverless
npm install serverless-python-requirements # In this dir
```

