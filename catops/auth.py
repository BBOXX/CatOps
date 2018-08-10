"""Functions to authorise users of CatOps."""
import hashlib
import hmac
import time
from urllib.parse import parse_qs
from slacker import Slacker


def verify_request(event, slack_secret, timeout=True):
    """Verify that Lambda event came from Slack"""
    version = 'v0'
    request_headers = event.get('headers')
    timestamp = request_headers.get('X-Slack-Request-Timestamp')
    if timeout and abs(time.time() - float(timestamp)) > 60 * 5:
        # The request timestamp is more than five minutes from local time
        # It could be a replay attack, so let's ignore it
        return False, 'Request timeout'

    request_body = event.get('body')
    sig_basestring = '{0}:{1}:{2}'.format(version, timestamp, request_body)
    sig = hmac.new(
        slack_secret.encode('utf-8'),
        msg=sig_basestring.encode('utf-8'),
        digestmod=hashlib.sha256).hexdigest()

    my_signature = '{0}={1}'.format(version, sig).encode('utf-8')
    slack_signature = request_headers.get('X-Slack-Signature')
    slack_signature_encoded = slack_signature.encode('utf-8')

    if hmac.compare_digest(my_signature, slack_signature_encoded):
        # Validate body, check for missing fields
        # token, team_id, team_domain, channel_id, etc
        return True, 'Valid signature'
    return False, 'Invalid signature'


def get_user_slack(event, oauth, team_id=None, channel_id=None):
    """Check whether user exists and is in specified team and channel.

    Arguments:
        event       - AWS Lambda event
        oauth       - Slack OAUTH token
        team_id     - Slack team_id (workspace, i.e. BBOXX)
        channel_id  - Channel user must be in
    Returns:
        False, err_msg
        True, user_dict with id, name, team_id, channel_id, email
    """
    slack = Slacker(oauth)
    body = event.get('body')
    pbody = parse_qs(body)
    # Cache this
    users = slack.users.list().body.get('members')
    user_dict = {}
    for user in users:
        if not user.get('deleted'):
            user_dict[user.get('name')] = {
                'id': user.get('id'),
                'username': user.get('name'),
                'team_id': user.get('team_id'),
                'channel_id': user.get('channel_id'),
                'email': user['profile'].get('email')
            }
    username = pbody.get('user_name')[0]
    # check that user is in the right team
    if username not in user_dict:
        return False, "User not in workspace"
    if team_id and user_dict[username]['team_id'] != team_id:
        return False, "User not in specified team"
    if channel_id and user_dict[username]['channel_id'] != channel_id:
        return False, "User not in specified channel"
    return True, user_dict[username]
