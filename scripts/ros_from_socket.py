#!/usr/bin/env python


import rospy
import math
import time

# from sensor_msgs.msg import JointState
from std_msgs.msg import String

import socket




class JointStatePublisher():
    def __init__(self):
        UDP_IP = "127.0.0.1"
        UDP_PORT = 5005
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
        self.sock.bind((UDP_IP, UDP_PORT))

        rospy.init_node('blender_joint_state_publisher', anonymous=True)
        
        # rate = rospy.get_param('~rate', 20)
        r = rospy.Rate(20)

        # self.joint_states_pub = rospy.Publisher('/joint_states', JointState)
        self.joint_states_pub = rospy.Publisher('/hello', String)
        rospy.loginfo("Starting Blender Joint State Publisher at " + str(20) + "Hz")
       
        # while not rospy.is_shutdown():
        while 1:
            rospy.loginfo('here')
            self.publish_joint_states()

            # self.publish_joint_states()
            # r.sleep()
       
    def publish_joint_states(self):
        # msg = JointState()
        # msg.name = ['elbow']
        # msg.position = [self.get_elbow()]

        # msg.velocity = []
        # msg.effort = []
          
        rospy.loginfo('alive')
        msg = String()
        msg.data = self.get_elbow()

        # msg.header.stamp = rospy.Time.now()
        # msg.header.frame_id = 'base_link'

        self.joint_states_pub.publish(msg)

    def get_elbow(self):


        # angle = float(sys.stdin.readline())
        
        rospy.loginfo( 'getting' )

        data, addr = self.sock.recvfrom(1024) # buffer size is 1024 bytes

        angle = data
        rospy.loginfo( angle )

        return angle
        # D = bpy.data
        
        # vec1 = D.objects['Elbow1'].matrix_world.to_translation()
        # vec2 = D.objects['Elbow2'].matrix_world.to_translation()
        
        # su =  (vec1[0] - vec2[0])**2
        # su += (vec1[1] - vec2[1])**2
        # su += (vec1[2] - vec2[2])**2
        
        # su = math.sqrt(su)
        # return su




        
if __name__ == '__main__':
    try:
        s = JointStatePublisher()
        rospy.spin()
    except rospy.ROSInterruptException: pass
