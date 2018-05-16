#!/usr/bin/env python

import bpy
import math
import time

import socket
from struct import Struct


class BlenderPusher:

    def __init__(self):
        self.UDP_IP = "127.0.0.1"
        self.UDP_PORT = 5005
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 

        self.struct = Struct("fffffff")

        self.joints = [self.get_turret, 
                       self.get_shoulder, 
                       self.get_elbow, 
                       self.get_wrist_pitch, 
                       self.get_wrist_yaw, 
                       self.get_wrist_roll, 
                       self.get_grip]

    def push(self):
        # out = ';'.join((str(x()) for x in self.joints))
        # self.sock.sendto(out.encode() , (self.UDP_IP, self.UDP_PORT))
        out = self.struct.pack( *(x() for x in self.joints) )
        self.sock.sendto(out , (self.UDP_IP, self.UDP_PORT))


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
        return self.get_distance('Shoulder1', 'Shoulder2')

    def get_elbow(self):
        return self.get_distance('Elbow1', 'Elbow2')

    def get_wrist_pitch(self):
        return self.get_angle('Elbow2','WristCube', 'WristDown')

    def get_wrist_yaw(self):
        return self.get_angle('WristSide','WristCube', 'WristPointer')

    def get_wrist_roll(self):
        return 5

    def get_grip(self):
        return 6

    def get_offsets(self):
        pass
        # D = bpy.data
        # D.scenes['Scene'].arm_offsets.wrist_roll_offset

        # col.prop(scene.arm_offsets, "gripper_offset")
        # col.prop(scene.arm_offsets, "wrist_roll_offset")
        
        # col.prop(scene.arm_offsets, "wrist_R_offset")
        # col.prop(scene.arm_offsets, "wrist_L_offset")

        # col.prop(scene.arm_offsets, "elbow_offset")
        # col.prop(scene.arm_offsets, "shoulder_offset")
        # col.prop(scene.arm_offsets, "turret_offset")

if __name__ == '__main__':

    a = BlenderPusher()
    def callback(passedScene):
        a.push()
        
    bpy.app.handlers.scene_update_pre.append(callback)

        
