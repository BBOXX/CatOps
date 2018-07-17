# Slack Logger Handler

## Setup

### Lambda Setup

1. Check [serverless.yml](serverless.yml)
  - Correct service name
  - Correct aws credentials profile
  - Correct http path
2. Set env variables
```bash
export SLACKOAUTHTOKEN="<slack-oauth-token>"
```
4. Run `sls deploy`

### Slack setup
1. [Create a New Slack App.](https://api.slack.com/apps)
2. Add a Bot User

## Installing [serverless framework](https://serverless.com)

```bash
sudo apt-get install npm
sudo npm install -g serverless
serverless config credentials --provider aws --key AKIAIOSFODNN7EXAMPLE --secret wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY # add credentials
npm install serevrless-python-requirements
```

