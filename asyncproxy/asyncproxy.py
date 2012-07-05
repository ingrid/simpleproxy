#!/usr/bin/python

import Queue
import re
import socket
import sys
import threading

from Queue import Queue
from threading import Thread

var = {}
port = 8000
cache = {}

class Client(Thread):
    def __init__(self, client, address):
        self.client = client
        self.address = address
        threading.Thread.__init__(self)
    def run(self):
        print "Request recieved."
        client = self.client
        address = self.address
        client_data = client.recv(10240)
        if not client_data:
            client.close()
            return
        print "Request read"
        print 'client_data:'
        print client_data[:400]
        key = tuple(re.split(r"[\r\n]+", client_data)[0:2])
        if key in cache:
            pass
        print 'caching key:'
        print key
        print '-----'
        full_host_string = key[1][6:]
        host = full_host_string
        print 'host:', host
        host_port = 80
        host_sock = socket.socket()
        host_sock.connect((host, host_port))
        print 'send returns:'
        print host_sock.send(client_data.replace('I like dogs', 'I hate dogs'))
        print 'should equal:'
        print len(client_data)

        while True:
            host_data = host_sock.recv(1000)
            if not host_data:
                break
            print 'data from server recieved:', len(host_data)

            print 'amound of data sent to client:', client.send(host_data)
            print 'we should have just sent data...'
        host_sock.close()
        client.close()

class IOLoop(object):
    def __init__(self):
        self.conn_loop = Queue()
    def start(self):
        pass
    def stop():
        pass
        

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
