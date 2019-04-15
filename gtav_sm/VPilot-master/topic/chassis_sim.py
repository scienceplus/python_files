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
import time
#import rospy
from cyber_py import cyber

from modules.canbus.proto import chassis_pb2

state = 0
#gear_p = 0

def chassis_data(chassis,count,q,q2):
    global state
        #,gear_p
    chassis.header.timestamp_sec = time.time()
    chassis.header.module_name = 'chassis'
    chassis.header.sequence_num = count

    while q.empty():
        #print("q.empty")
        continue
    if q2.empty():
        chassis.driving_mode = state
    else:
        if q2.get() == 1:
            chassis.driving_mode = 1
        else:
            chassis.driving_mode = 0
    state = chassis.driving_mode
    #get gearposition  yyz
    #gear_p = chassis.GearPosition.gear_position
    chassis_list = q.get()

    chassis.throttle_percentage = chassis_list[0]
    chassis.brake_percentage = chassis_list[1]
    chassis.steering_percentage = -chassis_list[2]*100
    #chassis.steering_percentage = chassis_list[2]*100
    if chassis.steering_percentage > 100:
        chassis.steering_percentage = 100
    elif chassis.steering_percentage < -100:
        chassis.steering_percentage = -100
    #chassis.steering_percentage = 30
    chassis.speed_mps = chassis_list[3]

    return chassis

def chassis_simulation(q,q2,q3):
    cyber.init()
    #rospy.init_node("chassis_offline", anonymous=True)
    node = cyber.Node("chassis_offline")

    #chassis_pub = rospy.Publisher(
    #   "/apollo/canbus/chassis", chassis_pb2.Chassis, queue_size=1)
    chassis_pub = node.create_writer("/apollo/canbus/chassis",
                       chassis_pb2.Chassis)

    # generate chassis info
    chassis = chassis_pb2.Chassis()

    # send pose to /apollo/canbus/chassis
    count = 0
    #r = rospy.Rate(20)
    #while not rospy.is_shutdown():
    while not cyber.is_shutdown():
        now = time.time()
        chassis_pub.write(chassis_data(chassis,count,q,q2,q3))
        count += 1
        sleep_time = 0.05 - (time.time() - now)  
        if sleep_time > 0:
            time.sleep(sleep_time) 
        #r.sleep()
