#!/usr/bin/python
import os
import subprocess
import time
import re
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
        print "Request recieved."
        client_data = client.recv(10240) 
        print client_data
        key = tuple(re.split(r"[\r\n]+", client_data)[0:2])
        if key in cache:
            pass
        print key
        full_host_string = key[1][6:]
        host = full_host_string
        host_port = 80
        host_sock = socket.socket()
        host_sock.connect((host, host_port))
        host_sock.send(client_data)
        host_data = host_sock.recv(1024 * 1024)
        host_sock.close()
        client.send(host_data)
        client.close()

    return ret
if __name__ == "__main__":
    main()
