#!/usr/bin/env python 
import rospy
import time
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

prev_ns = -1.0
scan_time = 0
avg_count = 0

def callback(data):
	ns = data.header.stamp.secs * 1000000000.0 + data.header.stamp.nsecs
	global prev_ns
	global scan_time
	global avg_count
	if (prev_ns != -1):
		scan_time = (scan_time * avg_count + (ns - prev_ns)) / (avg_count + 1)
		avg_count += 1
		prev_ns = ns
	else: 
		prev_ns = ns
		avg_count += 1

	print(scan_time / 1000000000.0)
	

def calc_scan_time():
	rospy.init_node('autonom', anonymous=True)

	rospy.Subscriber("/mybot/front_laser/scan", LaserScan, callback) 
	
	rospy.spin()
	

if __name__ == '__main__':
	#try:
	calc_scan_time()
	#except rospy.ROSInterruptException: pass

