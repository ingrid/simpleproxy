# IO Loop.

import logging
import select
import time

import Stream

logger = logging.getLogger(__name__)

kq_timeout = 10
POLL_TIMEOUT = 2

class Loop(object):

    def __init__(self):
        self.streams = {}
        # Add epoll and other support.
        self.poll = KQ()
        self.curr_streams = {}

    def add_stream(self, file_descriptor, stream, events):
        self.curr_streams[file_descriptor] = stream
        self.poll.register(file_descriptor, events)

    def add_socket(self, socket, events):
        file_descriptor = socket.fileno;
        stream = Stream(socket)

        return self.add_stream(file_descriptor, stream, events)

    def run(self):
        self.stop = False

        while not self.stop:
            print "Polling..."
            events = self.poll.poll()
            print "Got events!"
            while events:
                file_descriptor, event = events.popitem()
                print "File descriptor: ", file_descriptor
                print "Event: ", event
            print "Sleeping..."
            time.sleep(POLL_TIMEOUT)

# A kqueue wrapper.
class KQ(object):
    def __init__(self):
        self.kq = select.kqueue()
        self.active = {}

    def fileno(self):
        return self.kq.fileno()

    def close(self):
        self.kq.close()

    def register(self, fd, events=[]):
        if fd in self.active.keys():
            print "File descriptor already registered. Passing."
            return
        print "Registering a new connection."
        self.active[fd] = events
        kevents = []
        kevents.append(select.kevent(fd.fileno(), events))
        print self.kq.control([], 0, None)

    def poll(self):
        # Currently returns one at a time.
        # Need to update active.
        events = self.kq.control(None, 1, None)
        return events
                
