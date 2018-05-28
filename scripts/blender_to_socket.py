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

        self.struct = Struct("f"*7 + "i"*7)

        self.joints = [self.get_turret, 
                       self.get_shoulder, 
                       self.get_elbow, 
                       self.get_wrist_pitch, 
                       self.get_wrist_yaw, 
                       self.get_wrist_roll, 
                       self.get_grip]

    def push(self):
        if self.get_grip() > 0:
            out = self.struct.pack( * ( tuple(x() for x in self.joints) + self.get_offsets()) )
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
        D = bpy.data
        return D.objects['Armature'].pose.bones['Turret'].matrix.to_euler()[2]

    def get_shoulder(self):
        return self.get_distance('Shoulder1', 'Shoulder2')

    def get_elbow(self):
        return self.get_distance('Elbow1', 'Elbow2')

    def get_wrist_pitch(self):
        return self.get_angle('Elbow2','WristCube', 'WristDown')

    def get_wrist_yaw(self):
        return self.get_angle('WristSide','WristCube', 'WristPointer')

    def get_wrist_roll(self):
        return 0
        # return self.get_angle('WristUp','WristPointer', 'GripperUp')

    def get_grip(self):
        D = bpy.data
        return D.objects['Armature'].pose.bones['Centered_Target'].scale[0]

    def get_offsets(self):
        D = bpy.data
        return (D.scenes['Scene'].arm_offsets.turret_offset,
                    D.scenes['Scene'].arm_offsets.shoulder_offset,
                    D.scenes['Scene'].arm_offsets.elbow_offset,
                    D.scenes['Scene'].arm_offsets.wrist_L_offset,
                    D.scenes['Scene'].arm_offsets.wrist_R_offset,
                    D.scenes['Scene'].arm_offsets.wrist_roll_offset,
                    D.scenes['Scene'].arm_offsets.gripper_offset)


if __name__ == '__main__':

    a = BlenderPusher()
    def callback(passedScene):
        a.push()
        
    bpy.app.handlers.scene_update_pre.append(callback)

        
