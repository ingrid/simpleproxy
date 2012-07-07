import select
import socket

foo = open("test.txt")
port = 8000
kq = select.kqueue()
foo_ke = select.kevent(foo, filter=select.KQ_FILTER_VNODE,
                       fflags=select.KQ_NOTE_DELETE | select.KQ_NOTE_WRITE)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((socket.gethostname(), port))
sock.listen(5)

sock_ke = select.kevent(foo, filter=select.KQ_FILTER_VNODE,
                       fflags=select.KQ_NOTE_DELETE | select.KQ_NOTE_WRITE)

kq.control([foo_ke], 0, None)

kq.control([sock_ke], 0, None)

while True:
    events = kq.control(None, 1, None)
    for event in events:
        if event.fflags & select.KQ_NOTE_DELETE:
            print "File deleted."
        elif event.fflags & select.KQ_NOTE_WRITE:
            print "File updated."
foo.close()
