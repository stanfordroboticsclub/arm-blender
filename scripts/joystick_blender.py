#!/usr/bin/env python

import rospy
import bpy
import numpy as np
import struct
from math import pi
from std_msgs.msg import String
from sensor_msgs.msg import Joy
from roboclaw import Roboclaw

def init(uart='/dev/TTYTHS0', baud=115200):        
    global rc
    rc = Roboclaw(uart, baud)
    rc.Open()
    
    global pub
    pub = rospy.Publisher('arm_motion', String, queue_size=10)
    rospy.Subscriber('joy', Joy, manual_control)
    rospy.init_node('base_motors', anonymous=True)
    rospy.spin()

def position_control(data):
    values = np.empty(4, dtype=np.int8)
    print(values)
    for i in xrange(4):
        values[i] = int(data.axes[i] * 63 + 64)

    target = bpy.data.objects['Armature'].pose.bones['Target'].location
    target.x += data.buttons[0]
    target.y += data.buttons[1]
    target.z += data.buttons[3]

    update_info()
        
def update_info(): #TODO actually make readable + useful updates
    print("doing stuff")
    enc1 = rc.ReadEncM1(TE_ADDR)
    enc2 = rc.ReadEncM2(TE_ADDR)
    print(enc1)
    print(enc2)
    """
    speed1 = rc.ReadSpeedM1(address)
    speed2 = rc.ReadSpeedM2(address)
        
    print("Encoder1:"),
    if(enc1[0]==1):
	print enc1[1],
	print format(enc1[2],'02x'),
    else:
	print "failed",
    print "Encoder2:",
    if(enc2[0]==1):
	print enc2[1],
	print format(enc2[2],'02x'),
    else:
	print "failed " ,
    print "Speed1:",
    if(speed1[0]):
	print speed1[1],
    else:
	print "failed",
    print("Speed2:"),
    if(speed2[0]):
	print speed2[1]
    else:
	print "failed "
    """
    str = "send something useful"
    #rospy.loginfo(str) #for debugging purposes
    pub.publish(str)
        
if __name__ == '__main__':
    init()
