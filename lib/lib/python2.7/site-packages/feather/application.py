from feather.dispatcher import Dispatcher

class InvalidApplication(Exception):
    pass

class Application(object):
    """An application is defined as a set of messages that will be generated and
    responded to by plugins, and a Dispatcher that handles communication between
    plugins.

    Applications expect, at the least, a Plugin that listens for 'APP_START',
    and one that generates 'APP_STOP'
    """

    def __init__(self, messages):
        """Create a new application that expects to have plugins that implement
        a listener and messager for each message in messages.
        """
        self.dispatcher = Dispatcher()

        self.needed_listeners = set(messages)
        self.needed_listeners.add('APP_START')

        self.needed_messengers = set(messages)
        self.needed_messengers.add('APP_STOP')

        self.valid = False

    def register(self, plugin):
        """Take a feather.plugin.Plugin and tell our dispatcher about it.

        Plugins are expected to provide a list of the messages that they
        listen for and generate. If registering this plugin makes it so we have
        at least one plugin listening for and generating our expected messages,
        set self.valid to true
        """
        self.needed_listeners -= plugin.listeners
        self.needed_messengers -= plugin.messengers

        if self.needed_messengers == self.needed_listeners == set():
            self.valid = True

        self.dispatcher.register(plugin)

    def start(self):
        """If we have a set of plugins that provide our expected listeners and
        messengers, tell our dispatcher to start up. Otherwise, raise
        InvalidApplication
        """
        if not self.valid:
            err = ("\nMessengers and listeners that still need set:\n\n"
                   "messengers : %s\n\n"
                   "listeners : %s\n") 
            raise InvalidApplication(err % (self.needed_messengers,
                                            self.needed_listeners))
        self.dispatcher.start()
        
