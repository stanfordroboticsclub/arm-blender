#!/usr/bin/env python


import rospy
import math
import time
import socket
from struct import Struct

from sensor_msgs.msg import JointState

class JointStatePublisher():
    def __init__(self):
        UDP_IP = "127.0.0.1"
        UDP_PORT = 5005
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
        self.sock.bind((UDP_IP, UDP_PORT))

        self.sock.setblocking(0)
        self.struct = Struct("fffffffiiiiiii")

        rospy.init_node('blender_joint_state_publisher', anonymous=True)
        
        rate = 5
        r = rospy.Rate(rate)

        self.joint_states_pub = rospy.Publisher('/joint_states', JointState, queue_size=10)
        rospy.loginfo("Starting Blender Joint State Publisher at " + str(rate) + "Hz")

        self.data = self.struct.pack(*([0]*14))

        while not rospy.is_shutdown():
            self.publish_joint_states()
            r.sleep()
       
    def publish_joint_states(self):
        msg = JointState()
        msg.name = ["turret",
                      "shoulder",
                      "elbow",
                      "wrist_pitch",
                      "wrist_yaw",
                      "wrist_roll",
                      "grip"]

        incoming_data = self.get_state()
        msg.position = incoming_data[:7]
        msg.velocity = []
        msg.effort = incoming_data[7:]
          
        msg.header.stamp = rospy.Time.now()
        msg.header.frame_id = 'base_link'

        self.joint_states_pub.publish(msg)

    def get_state(self):
        try:
            while 1:
                self.data = self.sock.recv(1024) # buffer size is 1024 bytes
        except socket.error:
            pass

        return self.struct.unpack(self.data)

        
if __name__ == '__main__':
    try:
        s = JointStatePublisher()
        rospy.spin()
    except rospy.ROSInterruptException: pass
