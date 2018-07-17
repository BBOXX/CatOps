"""Logging slack_handler which posts to a Slack channel."""
import json
import logging
import requests


class SlackHandler(logging.Handler):
    """Logger slack_handler which posts json log body to lambda_url."""
    lambda_url = None   # Lambda URL to post log entry to 

    def __init__(self, lambda_url, level=logging.NOTSET):
        super(SlackHandler, self).__init__(level=level)
        self.lambda_url = lambda_url

    def emit(self, record):
        log_entry = self.format(record)
        # If formatter returns json
        try:
            dict_entry = json.loads(log_entry)
            return requests.post(
                self.lambda_url,
                json={
                    "channels":dict_entry.get('channels'),
                    "message":dict_entry.get('message'),
                    "level":dict_entry.get('level'),
                    "time":dict_entry.get('time')
                },
                headers={"Content-type": "application/json"}
            )
        except ValueError as err:
            print(err)
            return requests.post(
                self.lambda_url,
                log_entry, headers={"Content-type": "application/json"}
            )


if __name__ == '__main__':
    # Constants
    FORMAT_STR = '{\
            "channels":["#bot_tests"],\
            "time":"%(asctime)s", \
            "level":"%(levelname)s", \
            "message":"%(message)s"}'
    FORMAT = logging.Formatter(FORMAT_STR)
    LAMBDA_URL = ''
    # Create logger

    logger = logging.getLogger('slack_logger')
    logger.setLevel(logging.DEBUG)

    # Custom slack_handler
    slack_handler = SlackHandler(lambda_url=LAMBDA_URL)
    slack_handler.setLevel(logging.DEBUG)
    slack_handler.setFormatter(FORMAT)
    logger.addHandler(slack_handler)

    # Test logging
    logger.debug('Debug from the logger.')
    logger.info('Info from the logger.')
    logger.warning('Warning from the logger.')
    logger.error('Error from the logger.')
    logger.critical('Critical from the logger.')

