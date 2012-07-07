# IO Loop.

import logging
import select
import socket
import time

from Stream import Stream
from Util import EventWrapper

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
        self.requests = {}
        self.responses = {}
        self.waiting = {}

    def add_stream(self, stream, events):
        self.curr_streams[stream.socket.fileno()] = stream
        self.poll.register(stream.socket.fileno(), events)
        self.active[stream.socket.fileno()] = stream.socket

    def add_socket(self, socket, events):
        stream = Stream(socket)
        return self.add_stream(stream, events)

    def run(self):
        self.stop = False

        while not self.stop:
            tic = time.time()
            print "Polling..."
            events = self.poll.poll()
            print "Got events!"
            while events:
                kevent = events.pop()
                event = kevent.filter
                file_discriptor = int(kevent.ident)
                sock = self.active[file_discriptor]
                if sock in self.listening_sockets:
                    print "New connection recieved."
                    client, address = sock.accept()
                    self.add_socket(client, select.KQ_FILTER_READ | select.KQ_FILTER_WRITE)
                    self.requests[client] = ""
                elif event & select.KQ_FILTER_READ:
                    print "Ready to read!"
                    # Read a ton and assume we have the full request until we figure out how to get a socket empty event/continue to read on socket empty.
                    while True:
                        try:
                            print self.requests[sock]
                            data = sock.recv(4069)
                            self.requests[sock] += data 
                        except socket.error:
                            print "Panic."
                            break
                        if not data:
                            break
                    # data = sock.recv(10)
                    print self.requests[sock]
                    print "Processing request..."
                    
                    if sock in self.waiting.keys():
                        resp_sock = self.waiting[self.active[file_descriptor]]
                        self.responses[resp_sock] = self.requests[sock]
                        self.add_socket(sock, select.KQ_FILTER_WRITE)
                elif event & select.KQ_FILTER_WRITE:
                    print "Ready to write!"
            print "Sleeping..."
            print "This iteration took: ", time.time() - tic
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

    def register(self, fd, events):
        if fd in self.active.keys():
            print "File descriptor already registered. Passing."
            return
        print "Registering a new connection."
        self.active[fd] = events
        kevents = []
        print events
        kevents.append(select.kevent(fd, events))
        print self.kq.control(kevents, 0, None)

    def poll(self):
        # Currently returns one at a time.
        # Need to update active.
        events = self.kq.control(None, 1, None)
        return events
                
