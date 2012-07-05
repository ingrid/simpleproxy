# IO Loop.

import logging
import select
import time

import Stream

logger = logging.getLogger(__name__)

kq_timeout = 1000

class Loop(object):

    def __init__(self):
        self.streams = {}
        # Add epoll and other support.
        self.queue = KQ()
        self.curr_streams = {}

    def add_stream(self, file_descriptor, stream):
        self.curr_streams[file_descriptor] = stream
        # Need an alias so epoll is used on norma Linux.
        self.queue.register(file_descriptor, stream)

    def add_socket(self, socket):
        file_descriptor = socket.fileno;
        stream = Stream(socket)

        return self.add_stream(file_descriptor, stream)

    def run(self):
        self.stop = False

        while not self.stop:
            print "Polling."
            events = select.poll()
            while events:
                file_descriptor, event = events.popitem()
                print "File descriptor: ", file_descriptor
                print "Event: ", event
            time.sleep(kq_timeout)

# A kqueue wrapper.
class KQ(object):
    def __init__(self):
        self.kq = select.kqueue()
        self.active = {}

    def fileno(self):
        return self.kq.fileno()

    def close(self):
        self.kq.close()

    def register(self, fd, events):
        if fd in self.active.keys():
            print "File descriptor already registered. Passing."
        self.active[fd] = events
                
