#!/usr/bin/env python


import math
import time
import socket
from struct import Struct


class SocketPrinter():
    def __init__(self):
        UDP_IP = "127.0.0.1"
        UDP_PORT = 5005
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
        self.sock.bind((UDP_IP, UDP_PORT))

        self.sock.setblocking(0)
        self.struct = Struct("f"*7 + "i"*7)

        self.data = self.struct.pack(*([0]*14))

        while 1:
            print self.get_state()
            time.sleep(1)
       
    def get_state(self):
        try:
            while 1:
                self.data = self.sock.recv(1024) # buffer size is 1024 bytes
        except socket.error:
            pass

        return self.struct.unpack(self.data)

        
if __name__ == '__main__':
    SocketPrinter()
