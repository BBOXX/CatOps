import unittest

class DispatcherTest(unittest.TestCase):
    def test_placeholder(self):
        self.assertEqual(1,1)


class PluginsTest(unittest.TestCase):
    def test_test(self):
        self.assertEqual(1,1)

if __name__=="__main__":
    unittest.main()
