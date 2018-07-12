CatOps
======
Highly trained cats for managing servers.

What is CatOps?
---------------

CatOps is a very simple NoOps framework for deploying your own ChatOps bot.

Commands you wish to add to your CatOps implementation are added to a `plugins`
folder in the same directory, and will then be automatically imported and callable
using the function name.

Features
--------

- Completely NoOps. 
- Easily extensible.
- Pay per invocation.
- Provider agnostic.

Example
--------

Python handler
^^^^^^^^^^^^^^^

.. code-block:: python

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


Example plugin
^^^^^^^^^^^^^^

.. code-block:: python

  """example.py - example plugin for ChatOps."""

  def hi(self):
      return "Meow!"


Serverless configuration
^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: yaml

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


Deploy
^^^^^^

:code:`serverless deploy`

See [examples](https://github.com/bboxx/catops/example/) for more.

Installation
============

.. code-block:: bash

  sudo apt-get install npm # install node
  sudo npm install -g serverless # install serverless
  npm install serverless-python-requirements # install serverless-python-requirements in the same directory as serverless.yml
  pip install catops


FAQ
===

