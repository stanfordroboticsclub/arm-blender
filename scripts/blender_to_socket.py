#!/usr/bin/env python

import bpy
import math
import time

import socket


class BlenderPusher:

    def __init__(self):
        self.UDP_IP = "127.0.0.1"
        self.UDP_PORT = 5005
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 

    def push(self):
        self.sock.sendto(str(self.get_elbow()).encode() , (self.UDP_IP, self.UDP_PORT))

    def get_elbow(self):
        D = bpy.data
        vec1 = D.objects['Elbow1'].matrix_world.to_translation()
        vec2 = D.objects['Elbow2'].matrix_world.to_translation()
        
        su =  (vec1[0] - vec2[0])**2
        su += (vec1[1] - vec2[1])**2
        su += (vec1[2] - vec2[2])**2
        
        su = math.sqrt(su)
        return su

if __name__ == '__main__':

    a = BlenderPusher()
    def callback(passedScene):
        a.push()
        
    bpy.app.handlers.scene_update_pre.append(callback)

        
