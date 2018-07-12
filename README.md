<h1 align="center" >CatOps</h1>

Highly trained cats for managing servers.

![Dedicated server support agent.](https://github.com/BBOXX/CatOps/blob/master/docs/catops.jpg)

## What is CatOps?

CatOps is a very simple NoOps framework for deploying your own ChatOps bot.

Commands you wish to add to your CatOps implementation are added to a `plugins`
folder in the same directory, and will then be automatically imported and callable
using the function name.


## Why CatOps?

- NoOps.
		- Deploy, rewrite, and redeploy FaaS easily with no worrying about setting up and managing servers.
		- Only charged when CatOps is called.

- Codify common maintenance procedures.
		- Perform high level actions without intimate low level knowledge.
		- Prevent errors doing complicated but routine tasks. 

- Unify documentation.
		- CatOps can act as a unified go-to location for help, merging/pooling all documentation into one place.

- Transparency.
		- Team members can see all actions taken by others in solving a problem. Organic learning.
		- No 'go-to' person for certain maintenance tasks.
		- Everyone aware of server changes. No-one surprised that the server is down if they see `/meow restart server` in the chat.
		- Spread knowledge; everyone becomes equally capable of solving problems.
		- Out of date help messages or documentation is more obvious to everyone.

- Context-aware suggestions, suggest actions and display help depending on context.
		- Docs/procedures/etc are useful, but can be too much to read through, hard to find, not up to date. 
		- Reduce clutter when trying to figure out next actions. 

- Reduce context switching.
    - No need for bash, Linux, ssh or VPN to fix most server issues.
    - No checking server logs.
    - Easily accesible and readble output.

- Control access.
		- Only gives necessary access, no unnecessary ssh-ing into production!

## Features

- Completely NoOps. 
- Easily extensible.
- Pay per invocation.
- Provider agnostic.

## Example

### Python handler

```python handler.py
from catops import dispatch
import json

def endpoint(event, context):
    # event = {'command':['meow', 'hi']} # example event passed to lambda
    params = event['command']
    try:
        s = dispatch(params)
    except Exception as err:
        s = str(err)
    response = {
        "statusCode": 200,
        "body": json.dumps(s)
    }
    return response
```

### Example plugin

```python plugins/example.py
"""example.py - example plugin for ChatOps."""

def hi(*args):
    return "Meow!"
```

### Serverless configuration

```yaml serverless.yml
service: CatOps

package:
  include:
    - handler.py
    - plugins/**

custom:
  pythonRequirements:
    slim: true

provider:
name: aws
runtime: python3.6
profile: serverless

functions:
  dispatcher:
    handler: handler.endpoint
    events:
      - http:
          path: ping
          method: get

plugins:
  - serverless-python-requirements
```

### Deploy and Test

```bash
serverless deploy
serverless invoke --function dispatcher --path /path/to/json/data --log
```

See [examples](https://github.com/bboxx/catops/example/) for more.


## Installation

```bash
sudo apt-get install npm
sudo npm install -g serverless
npm install serverless-python-requirements
pip install catops
```

Install `serverless-python-requirements` in the same dir as `serverless.yml`.

## Limitations

- Passive rather than active; needs to be triggered (e.g. by Slack slash commands)
- Limitations of FaaS
    - Max size (256MB for AWS Lambda)
    - Execution time limit (5 minute for AWS Lambda)
    - No state (recommend using a cloud-based database for state e.g. DynamoDB for AWS)

