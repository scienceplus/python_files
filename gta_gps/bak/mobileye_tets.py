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
#import sys
#import json
import time
import random
import rospy

from modules.drivers.proto import mobileye_pb2


def mobileye_data(mobileye,count,q):
    # mobileye.header.timestamp_sec = 1
    # mobileye.header.module_name = 2
    # mobileye.header.sequence_num = 3
    # mobileye.header.lidar_timestamp = 4
    # mobileye.header.camera_timestamp = 5
    # mobileye.header.radar_timstamp = 6
    # mobileye.header.version = 7
    # mobileye.header.status = 8
    # if q.empty():
    #     continue
    mobileye_list = q
    count = 0
    for data in mobileye_list:

        mobileye.header.timestamp_sec = time.time()
        mobileye.header.module_name = 'mobileye'
        mobileye.header.sequence_num = count    #YYZmodfy 1122
        return mobileye
        # outman = mobileye.details_739.add()
        # outman.obstacle_id = data.obstacle_id
        # outman.obstacle_pos_x = data.obstacle_x
        # outman.obstacle_pos_y = data.obstacle_y
        # outman.obstacle_rel_vel_x = data.obstacle_rel_vel_x
        # outman.obstacle_type = data.obstacle_type
        # outman.obstacle_status = data.obstacle_status
        #
        # outman = mobileye.details_73a.add()
        # outman.obstacle_length = data.obstacle_length
        # outman.obstacle_width = data.obstacle_width
    '''
        outman = mobileye.details_73b.add()
        outman.object_accel_x = data.obstacle_acc
        outman.obstacle_angle = data.obstacle_angle
    '''
       # return mobileye

def main():
    rospy.init_node("mobileye_offline", anonymous=True)
    mobileye_pub = rospy.Publisher(
        "/apollo/sensor/mobileye", mobileye_pb2.Mobileye, queue_size=1)
    # generate mobileye info
    mobileye = mobileye_pb2.Mobileye()

    # obstacles_list = []
    # obstacle_object = Obstacle(1,random.randint(10,20))
    # obstacles_list.append(obstacle_object)
    # q = obstacles_list
    #1,1,1,1,1,1,1,1,

    # send pose to /apollo/drivers/mobileye
    count = 0
    r = rospy.Rate(1)
    while not rospy.is_shutdown():
        mobileye_pub.publish(mobileye_data(mobileye,count,q))
        count += 1
        r.sleep()

#class Obstacle:
 #   def __init__(self,angle,acc):
        # self.obstacle_id = id_ob #range 0:63
        # self.obstacle_type = type_ob    #range 0:7 0-Vehicle 1-Truck 2-Bike 3-Ped 4-Bicycle 5-Unused
        # self.obstacle_x = x
        # self.obstacle_y = y
 #       self.obstacle_angle = angle  #range -327.68:327.68 Unit:degree
        # #obstacle_speed = speed
        # self.obstacle_length = length    #range 0:31 Unite:meter
        # self.obstacle_width = width  #range 0:12.5 Unite:meter
 #       self.obstacle_acc = acc
        # self.obstacle_rel_vel_x = rel_vel_x  #Longitudinal relative velocity
        # self.obstacle_status = status    #0-undefined 1-standing 2-stopped 3-moving 4-oncoming 5-parked 6-unused

        #id_ob,type_ob,x,y,length,width,,rel_vel_x,status

if __name__ == '__main__':
    main()


