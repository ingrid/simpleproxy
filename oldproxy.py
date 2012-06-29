#!/usr/bin/python
import os
import subprocess
import time
import socket
import sys
import mimetypes
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import utils, encoders
from gevent import monkey

#monkey.patch_all()

var = {}
port = 8000
cache = {}

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
        client_data = client.recv(1024) 
        if '\r\n' in client_data:
            key = tuple(client_data.split('\r\n')[0:2])
        elif '\n' in client_data:
            key = tuple(client_data.split('\n')[0:2])
        else:
            key = tuple(client_data.split('\r')[0:2])
        if key in cache:
            pass
        print key
        print key[1][6:].split(':')
        full_host_string = key[1][6:]
        if ":" in full_host_string:
            host, host_port = tuple(split(':'))
        else:
            host = full_host_string
            host_port = 80
        sock = socket.socket()
        sock.connect((host, host_port))
        print "Connected to host."
        host_data = sock.recv(1024)
        print host_data
        client.send(host_data)
        client.close()

    return ret
if __name__ == "__main__":
    main()
