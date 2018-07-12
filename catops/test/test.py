import unittest
import catops


class DispatcherTest(unittest.TestCase):
    def test_meow(self):
        self.assertEqual("Meow!", catops.dispatch(['meow']))
    def test_no_args(self):
        self.assertRaises(catops.parser.ArgumentParserError, catops.dispatch([]))

class PluginsTest(unittest.TestCase):
    def test_placeholder(self):
        self.assertEqual(1,1)

class ParseTest(unittest.TestCase):
    def test_exception(self):
        parser = catops.CatParser( description='Check parser raises exception instead of exiting.')
        parser.add_argument('test')
        self.assertRaises(catops.parser.ArgumentParserError, lambda: parser.parse_args([]))

if __name__=="__main__":
    unittest.main()
