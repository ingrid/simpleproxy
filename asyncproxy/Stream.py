# A stream wrapper to simplyfiy intergration with a IO loop.

import collections
import socket

class Stream(object):

    def __init__(self, socket):
        self.socket = socket
        self.socket.setblocking(False)
        self.read_buffer = collections.deque()
        self.write_buffer = collections.deque()

    def read(self):
        pass

    def write(self):
        pass
    
