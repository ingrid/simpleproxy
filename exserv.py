#!/usr/bin/env/python
import launcelot
import select

listen_sock = launcelot.setup()
sockets = { listen_sock.fileno(): listen_sock }

requests = {}
responses = {}

poll = select.poll()
poll.register(listen_sock, select.POLLIN)

while True:
    for fd, event in poll.poll():
        sock = sockets[fd]
        # Remove closed sockets from our list.
        if event & (select.POLLHUP | select.POLLERR | select.POLLNVAL):
            poll.unregister(fd)
            del sockets[fd]
            requests.pop(sock, None)
            responses.pop(sock, None)

        # Aceept connections from new sockets.
        elif sock is listen_sock:
            newsock
        
