#!/usr/bin/env python

###############################################################################
# Copyright 2017 The Apollo Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
###############################################################################
"""
For GTA5
"""
#import os
import sys
import time
import random
import Queue


#rospy for the subscriber
import rospy
#from std_msgs.msg import String

#gps
from modules.localization.proto import pose_pb2
from modules.localization.proto import localization_pb2

			
def gps_data(LocalizationEstimate,count):	
	
	#YYZmodfy 1122
	LocalizationEstimate.header.timestamp_sec = time.time()
	LocalizationEstimate.header.module_name = 'localization'
	LocalizationEstimate.header.sequence_num = count   
		
	#test = gps_test()
	#PointENU
	
	LocalizationEstimate.pose.position.x = random.random()
	
	LocalizationEstimate.pose.position.y = 2.0
	LocalizationEstimate.pose.position.z = 3.0
	
	#Quaternion
	LocalizationEstimate.pose.orientation.qx = 0.0
	LocalizationEstimate.pose.orientation.qy = 0.0
	LocalizationEstimate.pose.orientation.qz = 0.0
	LocalizationEstimate.pose.orientation.qw = 0.0
	
	#Point3D
	LocalizationEstimate.pose.linear_velocity.x = 0.0
	LocalizationEstimate.pose.linear_velocity.y = 0.0
	LocalizationEstimate.pose.linear_velocity.z = 0.0
		
	#Point3D
	LocalizationEstimate.pose.linear_acceleration.x = 0.0
	LocalizationEstimate.pose.linear_acceleration.y = 0.0
	LocalizationEstimate.pose.linear_acceleration.z = 0.0
	
	#Point3D
	LocalizationEstimate.pose.angular_velocity.x = 0.0
	LocalizationEstimate.pose.angular_velocity.y = 0.0
	LocalizationEstimate.pose.angular_velocity.z = 0.0
	
	LocalizationEstimate.pose.heading = 0.0
	
	#Point3D
	LocalizationEstimate.pose.linear_acceleration_vrf.x = 0.0
	LocalizationEstimate.pose.linear_acceleration_vrf.y = 0.0
	LocalizationEstimate.pose.linear_acceleration_vrf.z = 0.0
		
	#Point3D
	LocalizationEstimate.pose.angular_velocity_vrf.x = 0.0
	LocalizationEstimate.pose.angular_velocity_vrf.y = 0.0
	LocalizationEstimate.pose.angular_velocity_vrf.z = 0.0
		
	#Point3D
	LocalizationEstimate.pose.euler_angles.x = 0.0
	LocalizationEstimate.pose.euler_angles.y = 0.0
	LocalizationEstimate.pose.euler_angles.z = 0.0
	
	
	return LocalizationEstimate 		
	

def main():
	rospy.init_node("pose_offline",anonymous=True)
#	pose_pub = rospy.Publisher(
#		"/apollo/localization/pose",pose_pb2.Pose,queue_size=1)	
	pose_pub = rospy.Publisher(
		"/apollo/localization/pose",localization_pb2.LocalizationEstimate,queue_size=1)			
	#generate localization info
	LocalizationEstimate = localization_pb2.LocalizationEstimate()
	
	#send pose to /apollo/localization/pose
	count = 0
	r = rospy.Rate(1)
	while not rospy.is_shutdown():
		pose_pub.publish(gps_data(LocalizationEstimate,count))
		count += 1
		r.sleep()
	
if __name__ == '__main__':
	main()	


