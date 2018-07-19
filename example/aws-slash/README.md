# Serverless Slack Slash Command Responder

## Features

- Responds to Slash commands.
- Readable help message and argparser.
- Automagically import all 'plugins' from the `plugins/` folder.

## Setup

### Lambda Setup

1. serverless config credentials --provider aws --key AKIAIOSFODNN7EXAMPLE --secret wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY # add credentials
2. Check [serverless.yml](serverless.yml)
  - Correct service name
  - Correct aws credentials profile
  - Correct http path
3. Set token values in [tokens.yml](tokens.yml) (don't commit these to Git)
4. Run `sls deploy`

### Slack setup
1. [Create a New Slack App.](https://api.slack.com/apps)
2. Register a slash command URL, point it to POST url of Lambda function from `sls deploy`

## Installing [serverless framework](https://serverless.com)

```bash
sudo apt-get install npm
sudo npm install -g serverless
npm install serverless-python-requirements # In this dir
```

