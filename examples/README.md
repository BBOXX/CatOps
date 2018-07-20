# Examples

## Templates slash_command, slackbot, slack_logger

1. Install template files into target-dir
  ```bash
  meow install [--template] [--target-dir]
  ```
2. Set-up Slack
  - Create an app
  - Add a slash command / Slackbot event subscription
3. Update parameters
  - OAuth tokens and URL params in tokens.json.
  - Parameters in serverless.yml e.g. service name.
4. Install and run `serverless deploy`

## Install serverless

```bash
sudo apt-get install npm
sudo npm install -g serverless
npm install serverless-python-requirements
```

Install `serverless-python-requirements` in the same dir as `serverless.yml`.
