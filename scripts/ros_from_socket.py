#!/usr/bin/env python


import rospy
import math
import time
import socket

from sensor_msgs.msg import JointState

class JointStatePublisher():
    def __init__(self):
        UDP_IP = "127.0.0.1"
        UDP_PORT = 5005
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
        self.sock.bind((UDP_IP, UDP_PORT))

        self.sock.setblocking(0)

        rospy.init_node('blender_joint_state_publisher', anonymous=True)
        
        # rate = rospy.get_param('~rate', 20)
        r = rospy.Rate(20)

        self.joint_states_pub = rospy.Publisher('/joint_states', JointState, queue_size=10)
        rospy.loginfo("Starting Blender Joint State Publisher at " + str(20) + "Hz")

        self.data = "0;0;0;0;0;0;0"
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

        msg.position = self.get_state()
        msg.velocity = []
        msg.effort = []
          
        msg.header.stamp = rospy.Time.now()
        msg.header.frame_id = 'base_link'

        self.joint_states_pub.publish(msg)

    def get_state(self):
        try:
            while 1:
                self.data = self.sock.recv(1024) # buffer size is 1024 bytes
        except socket.error:
            pass

        return [float(x) for x in self.data.split(';')]

        
if __name__ == '__main__':
    try:
        s = JointStatePublisher()
        rospy.spin()
    except rospy.ROSInterruptException: pass
