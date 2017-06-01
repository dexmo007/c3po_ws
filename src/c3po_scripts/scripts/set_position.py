#!/usr/bin/env python
import rospy
import time
from gazebo_msgs import SetModelState
from gazebo_msgs.msg import ModelState
from geometry_msgs.msg import Twist, Pose

def move():
	rospy.init_node('set_position', anonymous=True)
	pub = rospy.ServiceProxy('/gazebo/set_model_state', SetModelState)
	
	msg = ModelState()

	msg.model_name = "mybot"

	pose = Pose()
	
	pose.position.x = 0
	pose.position.y = 0
	pose.position.z = 0
	pose.orientation.x = 0
	pose.orientation.y = 0
	pose.orientation.z = 0

	tw = Twist()

	tw.linear.x = 0
	tw.linear.y = 0
	tw.linear.z = 0
	tw.angular.x = 0
	tw.angular.y = 0
	tw.angular.z = 0

	msg.pose = pose
	msg.twist = tw
	msg.reference_frame = "world"


	pub.request.model_state = msg

if __name__ == '__main__':
	try:
		move()
	except rospy.ROSInterruptException: pass
