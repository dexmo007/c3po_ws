#!/usr/bin/env python 
import rospy
import time
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

PI = 3.1415926535897
velocity_publisher = rospy.Publisher('/mybot/cmd_vel', Twist, queue_size=10)

def rotate(degrees, rechts):
	vel_msg = Twist()
	speed = 45
	angle = degrees
	#Converting from angles to radians
	angular_speed = speed*PI/180
	relative_angle = angle*PI/180

	vel_msg.linear.x=0
	vel_msg.linear.y=0
	vel_msg.linear.z=0
	vel_msg.angular.x = 0
	vel_msg.angular.y = 0

	# Checking if our movement is CW or CCW
	if rechts:
		vel_msg.angular.z = -abs(angular_speed)
	else:
		vel_msg.angular.z = abs(angular_speed)
	# Setting the current time for distance calculus
	t0 = rospy.Time.now().to_sec()
	current_angle = 0

	while(current_angle < relative_angle):
		velocity_publisher.publish(vel_msg)
		t1 = rospy.Time.now().to_sec()
		current_angle = angular_speed*(t1-t0)


	#Forcing our robot to stop
	vel_msg.angular.z = 0
	velocity_publisher.publish(vel_msg)

def moveStraight(distance):
	vel_msg = Twist()
	speed = 0.5
	#distance = 1
	vel_msg.linear.x = abs(speed)

	vel_msg.linear.y = 0
	vel_msg.linear.z = 0
	vel_msg.angular.x = 0
	vel_msg.angular.y = 0
	vel_msg.angular.z = 0

	#while not rospy.is_shutdown():

	#Setting the current time for distance calculus
	t0 = rospy.Time.now().to_sec()
	current_distance = 0

	#Loop to move the turtle in an specified distance
	while(current_distance < distance):
		#Publish the velocity
		velocity_publisher.publish(vel_msg)
		#Takes actual time to velocity calculus
		t1=rospy.Time.now().to_sec()
		#Calculates distancePoseStamped
		current_distance= speed*(t1-t0)
	#After the loop, stops the robot
	vel_msg.linear.x = 0
	#Force the robot to stop
	velocity_publisher.publish(vel_msg)


def callback(data):
	#for x in range(0, 1000):
		#rospy.loginfo("x: %i    %f", x, data.ranges[x]) 
	
	
	#0 = ganz rechts
	#239 = ganz links
	# 120 = mitte
	rangeRight = data.ranges[0]
	rangeCentral = data.ranges[120]
	rangeLeft = data.ranges[239] #todo take a few values

	msg = Twist()

	msg.linear.x = 0.5

	msg.linear.y = 0
	msg.linear.z = 0
	msg.angular.x = 0
	msg.angular.y = 0
	msg.angular.z = 0

	if (rangeCentral < 5 or rangeRight < 3 or rangeLeft < 3):
		msg.angular.z = PI/4 if rangeRight < rangeLeft else -PI/4

	velocity_publisher.publish(msg)
	

def autonom():
	rospy.init_node('autonom', anonymous=True)

	rospy.Subscriber("/mybot/front_laser/scan_filtered", LaserScan, callback) 
	
	rospy.spin()
	

if __name__ == '__main__':
	#try:
	autonom()
	#except rospy.ROSInterruptException: pass

