#!/usr/bin/python
import re
import socket
import threading
import sys

from threading import Thread

var = {}
port = 8000
cache = {}
debug = True

#import logging
#logger = logging.getLogger('simpleproxy')
#hdlr = logging.FileHandler('/var/tmp/myapp.log')
#formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
#hdlr.setFormatter(formatter)
#logger.addHandler(hdlr) 
#logger.setLevel(logging.WARNING)


class Client(Thread):
    def __init__(self, client, address):
        self.client = client
        self.address = address
        threading.Thread.__init__(self)
        self.daemon = True
    def run(self):
        client = self.client
        address = self.address
        client_data = client.recv(10240)
        if not client_data:
            client.close()
            return
        if debug:
            print 'Request:\n'
            print client_data[:400]
            print '\n\n\n'
        key = tuple(re.split(r"[\r\n]+", client_data)[0:2])
        if key in cache:
            print "Cache hit: ", key
            print '\n\n\n'
        if debug:
            print 'Caching Key:\n'
            print key
            print '\n\n\n'
        else:
            print key
        full_host_string = key[1][6:]
        host = full_host_string
        host_port = 80
        host_sock = socket.socket()
        host_sock.connect((host, host_port))
        host_sock.send(client_data.replace('I like dogs', 'I hate dogs'))
        response = []
        while True:
            host_data = host_sock.recv(1000)
            response.append(host_data)
            if not host_data:
                break
            client.send(host_data)
        if debug:
            print "Response:\n"
            print ''.join(response)
            print '\n\n\n'

        host_sock.close()
        client.close()

def main():
    argv = sys.argv
    var['root'] = "."
    if len(argv) > 1:
        var['root'] = argv[1]
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serversocket.bind((socket.gethostname(), port))
    print "Hostname:", socket.gethostbyname(socket.gethostname())
    print "Connected on port", port
    serversocket.listen(5)

    while 1:
        client, address = serversocket.accept()
        Client(client, address).start()

if __name__ == "__main__":
    main()
