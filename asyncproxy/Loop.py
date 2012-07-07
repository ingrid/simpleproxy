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
        self.listening_sockets = []
        self.active = {}

    def add_stream(self, file_descriptor, stream, events):
        self.curr_streams[file_descriptor] = stream
        self.poll.register(file_descriptor, events)
        self.active[fd] = stream.socket

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
                sock = active[file_discriptor]
                if active[file_discriptor] in self.listening_sockets:
                    print "New connection recieved."
                    client, address = sock.accept()
                    self.add_socket(socket, select.KQ_FILTER_READ | select.KQ_FILTER_WRITE)
                elif event.filter & select.KQ_FILTER_READ:
                    print "Ready to read!"
                elif event.filter & select.KQ_FILTER_WRITE:
                    print "Ready to write!"
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
                
