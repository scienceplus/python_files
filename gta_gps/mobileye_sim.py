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
#import random
import rospy

from modules.drivers.proto import mobileye_pb2


def mobileye_data(mobileye,count,q):
    mobileye.header.timestamp_sec = time.time()
    mobileye.header.module_name = 'mobileye'
    mobileye.header.sequence_num = count

    while q.empty():
        continue

    mobileye_list = q.get()

    del mobileye.details_739[:]
    del mobileye.details_73a[:]
    del mobileye.details_73b[:]

    if len(mobileye_list) == 0:
        return mobileye

    for data in mobileye_list:
        outman = mobileye.details_739.add()
        outman.obstacle_id = data.obstacle_id
        outman.obstacle_pos_x = data.obstacle_x
        outman.obstacle_pos_y = data.obstacle_y
        outman.obstacle_rel_vel_x = data.obstacle_rel_vel_x
        outman.obstacle_type = data.obstacle_type
        outman.obstacle_status = data.obstacle_status

        outman = mobileye.details_73a.add()
        outman.obstacle_length = data.obstacle_length
        outman.obstacle_width = data.obstacle_width

        outman = mobileye.details_73b.add()
        outman.object_accel_x = data.obstacle_acc
        outman.obstacle_angle = data.obstacle_angle
		
	return mobileye

def mobileye_simulation(q):
    rospy.init_node("mobileye_offline", anonymous=True)
    mobileye_pub = rospy.Publisher(
        "/apollo/sensor/mobileye", mobileye_pb2.Mobileye, queue_size=1)
    # generate mobileye info
    mobileye = mobileye_pb2.Mobileye()

    # send pose to /apollo/drivers/mobileye
    count = 0
    r = rospy.Rate(10)
    while not rospy.is_shutdown():
        mobileye_pub.publish(mobileye_data(mobileye,count,q))
        count += 1
        r.sleep()

