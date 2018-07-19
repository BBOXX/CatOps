"""Logging.Handler subclass which posts to AWS Lambda which posts to a Slack channel."""
from catops import SlackHandler

def test():
    # Constants
    with open('tokens.json', 'r') as stream:
        TOKENS = json.load(stream)
    LAMBDA_URL = TOKENS['SlackLambdaURL']

    # Create logger
    logger = logging.getLogger('slack_logger')
    logger.setLevel(logging.DEBUG)

    # Custom slack_handler
    slack_handler = SlackHandler(lambda_url=LAMBDA_URL)
    slack_handler.setLevel(logging.DEBUG)
    logger.addHandler(slack_handler)

    # Test logging
    logger.debug('Debug from the logger.')
    logger.info('Info from the logger.')
    logger.warning('Warning from the logger.')
    logger.error('Error from the logger.')
    logger.critical('Critical from the logger.')


if __name__ == '__main__':
    test()
