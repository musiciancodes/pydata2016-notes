from collections import defaultdict
from multiprocessing import Queue

class Dispatcher(object):
    """Recieve messages from Plugins and send them to the Plugins that listen
    for them.
    """
    def __init__(self):
        """Create our set of listeners, communication Queue, and empty set of
        plugins.
        """
        self.listeners = defaultdict(set)
        self.plugins = set()
        self.messages = Queue()

    def register(self, plugin):
        """Add the plugin to our set of listeners for each message that it
        listens to, tell it to use our messages Queue for communication, and
        start it up.
        """
        for listener in plugin.listeners:
            self.listeners[listener].add(plugin)
        self.plugins.add(plugin)
        plugin.messenger = self.messages
        plugin.start()

    def start(self):
        """Send 'APP_START' to any plugins that listen for it, and loop around
        waiting for messages and sending them to their listening plugins until
        it's time to shutdown.
        """
        self.recieve('APP_START')
        self.alive = True
        while self.alive:
            message, payload = self.messages.get()
            if message == 'APP_STOP':
                for plugin in self.plugins:
                    plugin.recieve('SHUTDOWN')
                self.alive = False
            else:
                self.recieve(message, payload)

    def recieve(self, message, payload=None):
        for listener in self.listeners[message]:
            listener.recieve(message, payload)



        
