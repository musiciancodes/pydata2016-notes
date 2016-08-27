import unittest
from feather import Dispatcher, Plugin, Application

class PrintFoo(Plugin):
    listeners = set(['APP_START', 'CALL_FOO'])

    messengers = set(['FOO'])
    
    def recieve(self, message, payload):
        print 'MMM, FOO'
        self.send('FOO', 'YEEEAHH')

class SendFoo(Plugin):
    listeners = set(['FOO'])
    messengers = set(['CALL_FOO', 'APP_END'])

    def __init__(self):
        self.i = 0

    def recieve(self, message, payload):
        self.i += 1
        print "SEND FOO %s" % self.i
        if self.i < 100:
            self.send('CALL_FOO')
        else:
            self.send('APP_STOP')
            
class DispatcherTest(unittest.TestCase):
    def setUp(self):
        self.dis = Dispatcher()
        self.printfoo = PrintFoo()


