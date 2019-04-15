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
# import os
import sys
import time
import random
# rospy for the subscriber
import rospy

# localization
from modules.localization.proto import pose_pb2
from modules.localization.proto import localization_pb2
#YYZTEST1119

def gps_list(LocalizationEstimate,count,q):
    # YYZmodfy 1122
    LocalizationEstimate.header.timestamp_sec = time.time()
    LocalizationEstimate.header.module_name = 'localization'
    LocalizationEstimate.header.sequence_num = count

    while q.empty():
        continue

    gps_list = q.get()


    # PointENU

    LocalizationEstimate.pose.position.x = gps_list[0]
    LocalizationEstimate.pose.position.y = gps_list[1]
    LocalizationEstimate.pose.position.z = gps_list[2]
    '''
    # Quaternion
    pose.orientation.qx = 0.0
    pose.orientation.qy = 0.0
    pose.orientation.qz = 0.0
    pose.orientation.qw = 0.0
    '''
    # Point3D
    LocalizationEstimate.pose.linear_velocity.x = gps_list[3]
    LocalizationEstimate.pose.linear_velocity.y = gps_list[4]
    LocalizationEstimate.pose.linear_velocity.z = gps_list[5]

    # Point3D
    LocalizationEstimate.pose.linear_acceleration.x = gps_list[6]
    LocalizationEstimate.pose.linear_acceleration.y = gps_list[7]
    LocalizationEstimate.pose.linear_acceleration.z = gps_list[8]

    # Point3D
    LocalizationEstimate.pose.angular_velocity.x = gps_list[9]
    LocalizationEstimate.pose.angular_velocity.y = gps_list[10]
    LocalizationEstimate.pose.angular_velocity.z = gps_list[11]

    LocalizationEstimate.pose.heading = gps_list[12]

    # Point3D
    LocalizationEstimate.pose.linear_acceleration_vrf.x = gps_list[13]
    LocalizationEstimate.pose.linear_acceleration_vrf.y = gps_list[14]
    LocalizationEstimate.pose.linear_acceleration_vrf.z = gps_list[15]
    '''
    # Point3D
    pose.angular_velocity_vrf.x = 0.0
    pose.angular_velocity_vrf.y = 0.0
    pose.angular_velocity_vrf.z = 0.0

    # Point3D
    pose.euler_angles.x = 0.0
    pose.euler_angles.y = 0.0
    pose.euler_angles.z = 0.0
    '''
    return LocalizationEstimate



def gnss_simulation(q):
	rospy.init_node("pose_offline",anonymous=True)
    localization_pub = rospy.Publisher(
		"/apollo/localization/pose",localization_pb2.LocalizationEstimate,queue_size=1)
	#generate localization info
    LocalizationEstimate = localization_pb2.LocalizationEstimate()

	#send pose to /apollo/localization/pose
    count = 0
	r = rospy.Rate(1)
	while not rospy.is_shutdown():
        localization_pub.publish(gps_list(LocalizationEstimate,count,q))
        count += 1
		r.sleep()



