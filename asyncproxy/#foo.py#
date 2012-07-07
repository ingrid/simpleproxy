import select

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
        self.kq.control(fd, events, select.KQ_EV_DELETE)
        del self.curr[fd]

    def poll(self):
        # Currently returns one at a time.                                                                                                                                         
        # Need to update active.                                                                                                                                                   
        events = self.kq.control(None, 1, None)
        return events


kq = KQ()

foo = open("foo")

kq.register(foo, select.KQ_FILTER_WRITE)


while True:
    events = kq.poll()
    for event in events:
        print event.ident
        if event.filter & select.KQ_FILTER_WRITE:
            print "File updated."
        else:
            print "Random event."

                       
