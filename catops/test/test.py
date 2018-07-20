import os
import unittest
import catops

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
HELP_MSG = """usage: 
                <command> [<args>]

                commands:
                    help
                    ping\n                    nested\n                    cat\n                    dog 
            

positional arguments:
  command  Subcommand to run
"""


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


class ParseTest(unittest.TestCase):
    def test_exception(self):
        parser = catops.CatParser(description = 'Check parser raises exception instead of exiting.')
        parser.add_argument('test')
        self.assertRaises(catops.parser.ArgumentParserError, lambda: parser.parse_args([]))

class InstallTest(unittest.TestCase):
    def test_install(self):
        BASE_DIR = 'test_dir'
        catops.install(['meow','install', '-t', 'slash_command', '-d', BASE_DIR])
        files = ['handler.py', 'tokens.json', 'package.json', 'package-lock.json', 'serverless.yml', 'README.md', 'requirements.txt']
        for f in files:
            path = '{0}/{1}'.format(BASE_DIR, f)
            print('Checking {} exists.'.format(path))
            self.assertTrue(os.path.isfile(path))
            os.remove(path)
        os.rmdir(BASE_DIR)
        


if __name__=="__main__":
    unittest.main()
