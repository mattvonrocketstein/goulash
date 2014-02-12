""" goulash.stdout
"""

import sys
import threading
from Queue import Queue, Empty

class ThreadedStdout(object):
    """ """
    def __init__(self, stdout=None):
        self.stdout = stdout if stdout is not None else sys.stdout
        self.registry = {}

    def install(self):
        if sys.stdout != self:
            sys.stdout = self

    def __getattr__(self, x):
        return getattr(self.stdout, x)

    def register(self, thread):
        q = Queue()
        self.registry[thread] = q
        return q

    def read_all(self, thread):
        result = ""
        q = self.registry[thread]
        while q.qsize():
            try:
                result += q.get(block=False)
            except Empty:
                pass
        return result

    def write(self, data):
        this = threading.current_thread()
        if this in self.registry:
            self.registry[this].put(data)
        else:
            self.stdout.write(data)
