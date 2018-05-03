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

        self.joints = [self.get_turret, 
                       self.get_shoulder, 
                       self.get_elbow, 
                       self.get_wrist_pitch, 
                       self.get_wrist_yaw, 
                       self.get_wrist_roll, 
                       self.get_grip]

    def push(self):
        out = ';'.join((str(x()) for x in self.joints))
        self.sock.sendto(out.encode() , (self.UDP_IP, self.UDP_PORT))

    def get_distance(self, obj1, obj2):
        D = bpy.data
        vec1 = D.objects[obj1].matrix_world.to_translation()
        vec2 = D.objects[obj2].matrix_world.to_translation()
        return (vec1 - vec2).length

    def get_angle(self, obj1, center, obj2):
        D = bpy.data
        vecC = D.objects[center].matrix_world.to_translation()
        vec1 = D.objects[obj1].matrix_world.to_translation()
        vec2 = D.objects[obj2].matrix_world.to_translation()
        return (vec1 - vecC).angle(vec2 - vecC)

    def get_turret(self):
        return 1

    def get_shoulder(self):
        D = bpy.data
        vec1 = D.objects['Shoulder1'].matrix_world.to_translation()
        vec2 = D.objects['Shoulder2'].matrix_world.to_translation()
        
        su =  (vec1[0] - vec2[0])**2
        su += (vec1[1] - vec2[1])**2
        su += (vec1[2] - vec2[2])**2
        
        su = math.sqrt(su)
        return su


    def get_elbow(self):
        D = bpy.data
        vec1 = D.objects['Elbow1'].matrix_world.to_translation()
        vec2 = D.objects['Elbow2'].matrix_world.to_translation()
        
        su =  (vec1[0] - vec2[0])**2
        su += (vec1[1] - vec2[1])**2
        su += (vec1[2] - vec2[2])**2
        
        su = math.sqrt(su)
        return su

    def get_wrist_pitch(self):
        return 3

    def get_wrist_yaw(self):
        return 4

    def get_wrist_roll(self):
        return 5

    def get_grip(self):
        return 6

if __name__ == '__main__':

    a = BlenderPusher()
    def callback(passedScene):
        a.push()
        
    bpy.app.handlers.scene_update_pre.append(callback)

        
