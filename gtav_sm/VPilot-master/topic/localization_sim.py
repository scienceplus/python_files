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
#import rospy
from cyber_py import cyber
import math

# localization
from modules.localization.proto import pose_pb2
from modules.localization.proto import localization_pb2
#YYZTEST1119


def get_quaternion_to_rpy(x,y,z,w):
    roll = math.atan2(2*(wx+yz),1-2*(x*x+y*y))
    pitch = math.asin(2*(wy-zx))
    yaw = math.atan2(2*w*z + x*y,1-2*(y*y+z*z))
    return[roll,pitch,yaw]
    pass

def get_rpy_to_quaternion(roll,pitch,yaw):
    cosRoll = math.cos(roll*0.5)
    sinRoll = math.sin(roll*0.5)
    cosPitch = math.cos(pitch*0.5)
    sinPitch = math.sin(pitch*0.5)
    cosYaw = math.cos(yaw*0.5)
    sinYaw = math.sin(yaw*0.5)

    w = cosRoll*cosPitch*cosYaw + sinRoll*sinPitch*sinYaw
    x = sinRoll*cosPitch*cosYaw - cosRoll*sinPitch*sinYaw
    y = cosRoll*sinPitch*cosYaw + sinRoll*cosPitch*sinYaw
    z = cosRoll*cosPitch*sinYaw - sinRoll*sinPitch*cosYaw
    return[w,x,y,z]
    pass

def gps_list(LocalizationEstimate,count,q):
    # YYZmodfy 1122
    LocalizationEstimate.header.timestamp_sec = time.time()
    LocalizationEstimate.header.module_name = 'localization'
    LocalizationEstimate.header.sequence_num = count

    while q.empty():
        continue
    gps_list = q.get()


    # PointENU

    #LocalizationEstimate.pose.position.x = gps_list[0]
    #LocalizationEstimate.pose.position.y = gps_list[1]
    LocalizationEstimate.pose.position.x = gps_list[0]
    LocalizationEstimate.pose.position.y = gps_list[1]
    LocalizationEstimate.pose.position.z = gps_list[2]
    
    
    # Quaternion
    LocalizationEstimate.pose.orientation.qx = gps_list[16]
    LocalizationEstimate.pose.orientation.qy = gps_list[17]
    LocalizationEstimate.pose.orientation.qz = gps_list[18]
    LocalizationEstimate.pose.orientation.qw = gps_list[19]
    
    '''
    LocalizationEstimate.pose.orientation.qx = 0

    LocalizationEstimate.pose.orientation.qy = 0

    LocalizationEstimate.pose.orientation.qz = 0

    LocalizationEstimate.pose.orientation.qw = 0
    '''
    
    # Point3D
    
    LocalizationEstimate.pose.linear_velocity.x = gps_list[3]
    LocalizationEstimate.pose.linear_velocity.y = gps_list[4]
    LocalizationEstimate.pose.linear_velocity.z = gps_list[5]
    
    '''
    LocalizationEstimate.pose.linear_velocity.x = gps_list[4]
    LocalizationEstimate.pose.linear_velocity.y = -gps_list[3]
    LocalizationEstimate.pose.linear_velocity.z = gps_list[5]
    '''

    # Point3D
    
    LocalizationEstimate.pose.linear_acceleration.x = gps_list[6]
    LocalizationEstimate.pose.linear_acceleration.y = gps_list[7]
    LocalizationEstimate.pose.linear_acceleration.z = gps_list[8]
    
    '''
    if gps_list[3]==0 and gps_list[4]==0 and gps_list[5]==0:
        LocalizationEstimate.pose.linear_acceleration.x = 0
        LocalizationEstimate.pose.linear_acceleration.y = 0
        LocalizationEstimate.pose.linear_acceleration.z = 0
    else:
        LocalizationEstimate.pose.linear_acceleration.x = gps_list[7]
        LocalizationEstimate.pose.linear_acceleration.y = -gps_list[6]
        LocalizationEstimate.pose.linear_acceleration.z = gps_list[8]
    '''

    # Point3D
    
    LocalizationEstimate.pose.angular_velocity.x = gps_list[9]
    LocalizationEstimate.pose.angular_velocity.y = gps_list[10]
    LocalizationEstimate.pose.angular_velocity.z = gps_list[11]
    
    '''
    LocalizationEstimate.pose.angular_velocity.x = gps_list[10]
    LocalizationEstimate.pose.angular_velocity.y = -gps_list[9]
    LocalizationEstimate.pose.angular_velocity.z = gps_list[11]
    '''
    '''
    #LocalizationEstimate.pose.heading = math.pi/2 - (float(gps_list[12])/180)*math.pi
    theta = (float(gps_list[12])/180)*math.pi
    
    if theta >math.pi:
        theta = theta -2*math.pi
    
    LocalizationEstimate.pose.heading = theta
    #LocalizationEstimate.pose.heading = 0
    '''
    LocalizationEstimate.pose.heading = gps_list[12]


    # Point3D
    
    LocalizationEstimate.pose.linear_acceleration_vrf.x = -gps_list[13]
    LocalizationEstimate.pose.linear_acceleration_vrf.y = gps_list[14]
    LocalizationEstimate.pose.linear_acceleration_vrf.z = gps_list[15]
    #print("acc_vrf_y",-gps_list[13])
    #print("speed_acc_y",gps_list[23])
    '''
    if gps_list[3]==0 and gps_list[4]==0 and gps_list[5]==0:
        LocalizationEstimate.pose.linear_acceleration_vrf.x = 0
        LocalizationEstimate.pose.linear_acceleration_vrf.y = 0
        LocalizationEstimate.pose.linear_acceleration_vrf.z = 0
    else:
    '''
    '''
    LocalizationEstimate.pose.linear_acceleration_vrf.x = 0
    LocalizationEstimate.pose.linear_acceleration_vrf.y = gps_list[23]
    LocalizationEstimate.pose.linear_acceleration_vrf.z = 0
    '''
    
    #test
    # Point3D
    '''
    LocalizationEstimate.pose.angular_velocity_vrf.x = gps_list[9]
    LocalizationEstimate.pose.angular_velocity_vrf.y = gps_list[10]
    LocalizationEstimate.pose.angular_velocity_vrf.z = gps_list[11]
    '''

    LocalizationEstimate.pose.angular_velocity_vrf.x = gps_list[24]
    LocalizationEstimate.pose.angular_velocity_vrf.y = gps_list[25]
    LocalizationEstimate.pose.angular_velocity_vrf.z = gps_list[26]
    
    
    # Point3D
    LocalizationEstimate.pose.euler_angles.x = gps_list[20]
    LocalizationEstimate.pose.euler_angles.y = gps_list[21]
    LocalizationEstimate.pose.euler_angles.z = gps_list[22]
    
    '''
    LocalizationEstimate.pose.euler_angles.x = 0
    LocalizationEstimate.pose.euler_angles.y = 0
    LocalizationEstimate.pose.euler_angles.z = 0
    '''

    LocalizationEstimate.gtav.lc_position.x = gps_list[27]
    LocalizationEstimate.gtav.lc_position.y = gps_list[28]
    LocalizationEstimate.gtav.lc_position.z = 0
    LocalizationEstimate.gtav.width = gps_list[29]
    
    return LocalizationEstimate



def gnss_simulation(q):
    cyber.init()
    #rospy.init_node("pose_offline",anonymous=True)
    node = cyber.Node("pose_offline")

    #localization_pub = rospy.Publisher(
	#	"/apollo/localization/pose",localization_pb2.LocalizationEstimate,queue_size=1)
    localization_pub = node.create_writer("/apollo/localization/pose",
                       localization_pb2.LocalizationEstimate)

	#generate localization info
    LocalizationEstimate = localization_pb2.LocalizationEstimate()

	#send pose to /apollo/localization/pose
    count = 0
    #r = rospy.Rate(20)
    #while not rospy.is_shutdown():
    while not cyber.is_shutdown():
        now = time.time()
        #localization_pub.publish(gps_list(LocalizationEstimate,count,q))
        localization_pub.write(gps_list(LocalizationEstimate,count,q))  
        sleep_time = 0.05 - (time.time() - now)  
        if sleep_time > 0:
            time.sleep(sleep_time)       
        count += 1
	#r.sleep()



