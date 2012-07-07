# IO Loop.

import logging
import re
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
                print sock.getsockname()
                print sock.fileno()
                if sock in self.listening_sockets:
                    print "New connection recieved."
                    client, address = sock.accept()
                    self.add_socket(client, select.KQ_FILTER_READ)
                    self.requests[client] = ""
                    continue
                elif event & select.KQ_FILTER_READ:
                    print "Ready to read!"
                    # Read a ton and assume we have the full request until we figure out how to get a socket empty event/continue to read on socket empty.
                    if sock not in self.requests.keys():
                        self.requests[sock] = ""

                    while True:
                        try:
                            print "Reading..."
                            data = sock.recv(4069)
                            if not data:
                                break
                            self.requests[sock] += data 
                        except socket.error:
                            print "Panic."
                            break
                    if not self.requests[sock]:
                        # I do not know.
                        continue
                    # data = sock.recv(10)
                    # print self.requests[sock]
                    print "Processing request..."
                    print "File Descriptor: ", sock
                    print "Waiting: ", self.waiting.keys()
                    if sock not in self.waiting.keys():
                        print "Fresh request."
                        # This is a fresh request.
                        # Copypasta.
                        key = re.split(r"[\r\n]+", self.requests[sock])[0]
                        print "Req: ", self.requests[sock]
                        print "Key: ", key
                        full_host_string = key.split(" ")[1][7:]
                        print full_host_string 
                        host = full_host_string
                        if host.endswith("/"):
                            host = host[:-1]
                        host_port = 80
                        host_sock = socket.socket()
                        print "Connecting to host: ", host
                        print "Connecting to port: ", host_port
                        host_sock.connect((host, host_port))
                        
                        self.responses[host_sock] = self.requests[sock]
                        del self.requests[sock]
                        self.waiting[host_sock] = sock

                        host_sock.send(self.responses[host_sock])

                        self.add_socket(host_sock, select.KQ_FILTER_READ)
                        """
                        self.add_socket(host_sock, select.KQ_FILTER_WRITE)
                        # self.poll.unregister(sock.fileno())
                        """
                    if sock in self.waiting.keys():
                        """
                        resp_sock = self.waiting[sock]
                        self.responses[resp_sock] = self.requests[sock]
                        self.add_socket(sock, select.KQ_FILTER_WRITE)
                        """
                        # self.waiting[sock].send(self.responses[sock])
                        self.waiting[sock].send(data)
                        del self.responses[sock]
                        del self.waiting[sock]
                        self.poll.unregister(sock.fileno())
                elif event & select.KQ_FILTER_WRITE:
                    print "Ready to write!"
                    if self.responses[sock]:
                        sock.send(self.responses[sock])
                    if self.waiting[sock]:
                        self.add_socket(sock, select.KQ_FILTER_READ)
                    else:
                        sock.close()
            print "Sleeping..."
            print "This iteration took: ", time.time() - tic
            print "Waiting"
            print [k.fileno() for k in self.waiting.keys()]
            print "Requests"
            print [k.fileno() for k in self.requests.keys()]
            print "Active"
            print self.active.keys()
            print "Responses"
            print [k.fileno() for k in self.responses.keys()]
            print "Current"
            print self.curr_streams.keys()
            time.sleep(POLL_TIMEOUT)

# A kqueue wrapper.
class KQ(object):
    def __init__(self):
        self.kq = select.kqueue()
        self.active = {}
        self.curr = {}

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
        self.curr[fd] = events

    def unregister(self, fd):
        events = self.curr[fd]
        print "EVENTS: ", events
        self.kq.control([select.kevent(fd, events, select.KQ_EV_DELETE)], 0)
        del self.curr[fd]

    def poll(self):
        # Currently returns one at a time.
        # Need to update active.
        events = self.kq.control(None, 1, None)
        return events
                
