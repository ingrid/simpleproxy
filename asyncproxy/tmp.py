import select
import socket
import kqueue_event

port = 8000
host = socket.gethostname()

kq = select.kqueue()

foo = open("test.txt")
foo_ke = select.kevent(foo, filter=select.KQ_FILTER_VNODE | select.KQ_FILTER_READ | select.KQ_FILTER_WRITE,
                       flags=select.KQ_EV_ADD | select.KQ_EV_ENABLE | select.KQ_EV_CLEAR,
                       fflags=select.KQ_NOTE_DELETE | select.KQ_NOTE_WRITE)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((host, port))
sock.listen(5)

print "Host: ", socket.gethostbyname(host)
print "Port: ", port

#sock_ke = select.kevent(sock, select.KQ_FILTER_READ, select.KQ_EV_ADD | select.KQ_EV_ENABLE)
sock_ke = select.kevent(sock, select.KQ_FILTER_READ)

kq.control([foo_ke], 0, None)
kq.control([sock_ke], 0, None)
while True:
    events = kq.control(None, 1, None)
    for event in events:
        print event.ident
        if event.fflags & select.KQ_NOTE_DELETE:
            print "File deleted."
        elif event.fflags & select.KQ_NOTE_WRITE:
            print "File updated."
        else:
            print event.fflags
            print event.flags
            print event.filter
        print kqueue_event.EventWrapper(event)
        print '---'
#f.close()

