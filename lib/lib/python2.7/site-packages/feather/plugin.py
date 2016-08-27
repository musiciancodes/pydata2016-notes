from multiprocessing import Process, Queue

class InvalidArguments(ValueError):
    pass

class Plugin(Process):
    """A Plugin is a self-contained bit of functionality that runs in it's own
    process, and runs via listening for messages and sending messages through
    Queues.
    """
    listeners = set(['SHUTDOWN'])
    messengers = set([])
    name = 'Base Plugin'

    def __new__(cls, *args, **kwargs):
        plug = super(Plugin, cls).__new__(cls, *args, **kwargs)
        plug.listeners.update(Plugin.listeners)
        return plug

    def __init__(self):
        """Set us up to run as a separate process, initialze our listener Queue,
        and set our runnable attribute.
        """
        super(Plugin, self).__init__()
        self.listener = Queue()
        self.runnable = True

    def send(self, message, payload=None):
        """Send a message through our messenger Queue.
        Messages are presumably descriptions of a task that just got completed,
        or a notification of status, or whatnot.
        """
        self.messenger.put((message, payload))

    def recieve(self, message, payload=None):
        """Get a message from our listener Queue.
        This should currently be used in a subclasses self.run loop. 
        """
        self.listener.put((message, payload))

    def SHUTDOWN(self, payload):
        """Set self.runnable to false.
        This should cause a subclass to break out of it's run loop.
        """
        self.runnable=False

    def pre_run(self):
        """Code to be run before our run loop starts"""
        pass

    def pre_call_message(self):
        """Code to be run before calling a message handler"""
        pass

    def pre_first_call_message(self):
        """Code to be run before calling the first message handler"""

    def post_first_call_message(self):
        """Code to be run after the first message has been handled"""
        pass

    def post_call_message(self):
        """Code to be run after a message has been handled"""
        pass

    def post_run(self):
        """Code to be run after our run loop terminates"""
        pass
        
    def run(self):
        """Run our loop, and any defined hooks...
        """
        self.pre_run()
        first = True
        while self.runnable:
            self.pre_call_message()

            if first:
                self.pre_first_call_message()
            
            message, payload = self.listener.get()
            getattr(self, message)(payload)

            if first:
                first = False
                self.post_first_call_message()
                
            self.post_call_message()

        self.post_run()

