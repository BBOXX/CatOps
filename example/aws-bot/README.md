# Serverless Slack Bot

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

### Slack Setup

1. [Create a New Slack App.](https://api.slack.com/apps)
2. Add a Bot User
3. Event Subscriptions -> Enable Events
  - Enter the Request URL from running `sls deploy`.
