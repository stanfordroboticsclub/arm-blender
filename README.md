# arm-blender
Use Blender to control a robotic arm

###Install 

Make sure you have blender installed
`sudo apt install blender`

###Run
`roslaunch arm-blender blender.launch`

###What it does

Publishes a [Joint State](http://docs.ros.org/api/sensor_msgs/html/msg/JointState.html) message to topic `/joint_states` which corresponds to the joint positions set in the blender GUI

###NB

It uses port `5005`