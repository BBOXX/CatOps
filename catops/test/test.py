import unittest
import catops

HELP_MSG = """usage: 
                <command> [<args>]

                commands:
                   ping\nnested\ncat\ndog 
            

positional arguments:
  command     Subcommand to run

optional arguments:
  -h, --help  show this help message and exit\n"""


class DispatcherTest(unittest.TestCase):
    params={'user_name':['CatOps']}
    d = catops.Dispatcher()

    def test_meow(self):
        answer = {'statusCode':200, 'text':'@CatOps Meow!'}
        self.assertEqual(answer, catops.dispatch('meow'))


    def test_no_args(self):
        self.assertRaises(catops.parser.ArgumentParserError, lambda: self.d.parse_command('', self.params))
        self.assertRaises(catops.parser.ArgumentParserError, lambda: catops.dispatch(''))
        # Test dispatch function
        try:
            catops.dispatch('')
        except catops.parser.ArgumentParserError as err:
            self.assertEqual('the following arguments are required: command', str(err))
        # Test Dispatcher().parse_command function
        try:
            self.d.parse_command('', self.params)
        except catops.parser.ArgumentParserError as err:
            self.assertEqual('the following arguments are required: command', str(err))


    def test_invalid_args(self):
        try:
            catops.dispatch('hi')
        except catops.parser.ArgumentParserError as err:
            self.assertEqual('Unrecognized command: hi\n{}'.format(HELP_MSG), str(err))
        try:
            self.d.parse_command('hi', self.params)
        except catops.parser.ArgumentParserError as err:
            self.assertEqual('Unrecognized command: hi\n{}'.format(HELP_MSG), str(err))


class PluginsTest(unittest.TestCase):
    def test_plugins(self):
        catops.Dispatcher(plugin_dir = 'plugins/')


class ParseTest(unittest.TestCase):
    def test_exception(self):
        parser = catops.CatParser(description = 'Check parser raises exception instead of exiting.')
        parser.add_argument('test')
        self.assertRaises(catops.parser.ArgumentParserError, lambda: parser.parse_args([]))


if __name__=="__main__":
    unittest.main()
