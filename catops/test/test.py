import os
import sys
import unittest
import catops

abspath = os.path.normpath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

HELP_MSG = """usage: 
                <command> [<args>]

                commands:
                    help
                    cat\n                    dog\n                    nested\n                    ping
            

positional arguments:
  command  Subcommand to run
"""


class DispatchTest(unittest.TestCase):
    def test_include_functions(self):
        self.assertEqual(
            True,
            bool(catops.dispatch(command='cat', include_functions=['cat']))
        )

        self.assertRaises(
            catops.parser.ArgumentParserError,
            lambda: catops.dispatch(command='dog', include_functions=['cat'])
        )

    def test_convert_dispatch(self):
        self.assertEqual(
            'Meow meow.',
            catops.convert_dispatch({'text':'cat'}, include_functions=['cat'])['attachments'][0]['fallback']
        )
        title='Invalid command: /catops dog'
        self.assertEqual(
            title,
            catops.convert_dispatch({'text':'dog'}, include_functions=['cat'])['attachments'][0]['title']
        )

class DispatcherTest(unittest.TestCase):
    params={'user_name':['CatOps']}
    d = catops.Dispatcher() 

    def test_meow(self):
        answer = {'statusCode':200, 'text':'@CatOps Meow!'}
        self.assertEqual(answer, catops.dispatch('meow'))

    def test_no_args(self):
        self.assertRaises(catops.parser.ArgumentParserError, lambda: self.d.parse_command('', self.params))
        self.assertRaises(catops.parser.ArgumentParserError, lambda: catops.dispatch(''))
        # Test dispatch function try: catops.dispatch('') except catops.parser.ArgumentParserError as err: self.assertEqual('the following arguments are required: command', str(err))
        # Test Dispatcher().parse_command function
        try:
            self.d.parse_command('', self.params)
        except catops.parser.ArgumentParserError as err:
            if (sys.version_info < (3,0)):
                self.assertEqual('too few arguments', str(err))
            else:
                self.assertEqual('the following arguments are required: command', str(err))


    def test_invalid_args(self):
        try:
            catops.dispatch('hi')
        except catops.parser.ArgumentParserError as err:
            self.assertEqual('{}'.format(HELP_MSG), str(err))
        try:
            self.d.parse_command('hi', self.params)
        except catops.parser.ArgumentParserError as err:
            self.assertEqual('{}'.format(HELP_MSG), str(err))


class PluginsTest(unittest.TestCase):
    def test_plugins(self):
        catops.Dispatcher(plugin_dir = 'plugins/')

    def test_include_functions(self):
        d1 = catops.Dispatcher(include_functions=['cat'])
        self.assertTrue(
            'dog' not in d1.functions and
            'cat' in d1.functions
        )
        d2 = catops.Dispatcher(include_functions=['dog'])
        self.assertTrue(
            'dog' in d2.functions and
            'cat' not in d2.functions
        )

class ParseTest(unittest.TestCase):
    def test_exception(self):
        parser = catops.CatParser(description = 'Check parser raises exception instead of exiting.')
        parser.add_argument('test')
        self.assertRaises(catops.parser.ArgumentParserError, lambda: parser.parse_args([]))


class SlackPayload(unittest.TestCase):
    def test_create_payload(self):
        test_payload = {
            'statusCode': '200',
            'headers': {'Content-Type': 'application/json'},
            'response_type': 'in_channel',
            'text': 'hullo friend'
        }
        payload = catops.create_slack_payload(
            'in_channel',
            text='hullo friend'
        )
        self.assertEqual(payload, test_payload)
    def test_create_attachment(self):
        test_attachment = {
            "fallback": "Required plain-text summary of the attachment.",
            "color": "#2eb886",
            "pretext": "Optional text that appears above the attachment block",
            "author_name": "Bobby Tables",
            "author_link": "http://flickr.com/bobby/",
            "author_icon": "http://flickr.com/icons/bobby.jpg",
            "title": "Slack API Documentation",
            "title_link": "https://api.slack.com/",
            "text": "Optional text that appears within the attachment",
            "fields": [
                {
                    "title": "Priority",
                    "value": "High",
                    "short": False
                }
            ],
            "image_url": "http://my-website.com/path/to/image.jpg",
            "thumb_url": "http://example.com/path/to/thumb.png",
            "footer": "Slack API",
            "footer_icon": "https://platform.slack-edge.com/img/default_application_icon.png",
            "ts": 123456789
        }
        attachment = catops.create_slack_attachment(
            fallback = "Required plain-text summary of the attachment.",
            color = "#2eb886",
            pretext = "Optional text that appears above the attachment block",
            author_name = "Bobby Tables",
            author_link = "http://flickr.com/bobby/",
            author_icon = "http://flickr.com/icons/bobby.jpg",
            title = "Slack API Documentation",
            title_link = "https://api.slack.com/",
            text = "Optional text that appears within the attachment",
            fields = [
                {
                    "title": "Priority",
                    "value": "High",
                    "short": False
                }
            ],
            image_url = "http://my-website.com/path/to/image.jpg",
            thumb_url = "http://example.com/path/to/thumb.png",
            footer = "Slack API",
            footer_icon = "https://platform.slack-edge.com/img/default_application_icon.png",
            ts = 123456789
        )
        self.assertEqual(test_attachment, attachment)
        test_payload = {
            'statusCode': '200',
            'headers': {'Content-Type': 'application/json'},
            'response_type': 'in_channel',
            'attachments': [test_attachment],
            'text': ''
        }
        payload = catops.create_slack_payload('in_channel', attachments=attachment)
        self.assertEqual(test_payload, payload)



if __name__=="__main__":
    unittest.main()
