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
import random
import rospy

from modules.canbus.proto import chassis_pb2


def chassis_data(chassis,count):
    chassis.header.timestamp_sec = time.time()
    chassis.header.module_name = 'chassis'
    chassis.header.sequence_num = count
    #chassis_list = q.get()


    chassis.throttle_percentage = random.random()

    #chassis.brake_percentage = chassis_list[1]

    #chassis.steering_percentage = chassis_list[2]

    return chassis

def main():
    rospy.init_node("chassis_offline", anonymous=True)
    chassis_pub = rospy.Publisher(
        "/apollo/canbus/chassis", chassis_pb2.Chassis, queue_size=1)
    # generate chassis info
    chassis = chassis_pb2.Chassis()

    # send pose to /apollo/canbus/chassis
    r = rospy.Rate(1)
    count = 0
    while not rospy.is_shutdown():
        chassis_pub.publish(chassis_data(chassis,count))
        count += 1
        r.sleep()
		


if __name__ == '__main__':
	main()
