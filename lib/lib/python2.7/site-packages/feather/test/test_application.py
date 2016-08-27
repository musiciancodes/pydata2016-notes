import unittest
from feather import Application, Plugin

class ApplicationTest(unittest.TestCase):

    def setUp(self):
        self.commands = set(['one', 'two', 'three', 'APP_START', 'APP_STOP'])
        self.app = Application(self.commands)
        
    def test_create_application(self):
        self.assertEqual(self.app.needed_listeners, self.commands)
        self.assertEqual(self.app.needed_messengers, self.commands)
        self.assertFalse(self.app.valid)
