#!/usr/bin/env python
import rospy
import time
from geometry_msgs.msg import Twist

def move():
	rospy.init_node('test_move', anonymous=True)
	velocity_publisher = rospy.Publisher('/mybot/cmd_vel', Twist, queue_size=10)
	vel_msg = Twist()

	speed = input("input your speed:")
	
	vel_msg.linear.y = 0
	vel_msg.linear.z = 0
	vel_msg.angular.x = 0
	vel_msg.angular.y = 0
	vel_msg.angular.z = 0

	#while not rospy.is_shutdown():
	vel_msg.linear.x = speed

	t0 = rospy.Time.now().to_sec()

	while (rospy.Time.now().to_sec() - t0 < 1):	
		velocity_publisher.publish(vel_msg)
		time.sleep(0.05)

	vel_msg.linear.x = 0
	velocity_publisher.publish(vel_msg)
	#break

if __name__ == '__main__':
	try:
		move()
	except rospy.ROSInterruptException: pass
