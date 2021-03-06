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

import sys

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
import rosbag
import rospy
from std_msgs.msg import String

from modules.canbus.proto import chassis_pb2
from modules.localization.proto import localization_pb2

GPS_X = list()
GPS_Y = list()
GPS_LINE = None
DRIVING_MODE_TEXT = ""
CHASSIS_TOPIC = "/apollo/canbus/chassis"
LOCALIZATION_TOPIC = "/apollo/localization/pose"
IS_AUTO_MODE = False


def chassis_callback(chassis_data):
    global IS_AUTO_MODE
    if chassis_data.driving_mode == chassis_pb2.Chassis.COMPLETE_AUTO_DRIVE:
        IS_AUTO_MODE = True
    else:
        IS_AUTO_MODE = False
    IS_AUTO_MODE = True
    DRIVING_MODE_TEXT = str(chassis_data.driving_mode)


def localization_callback(localization_data):
    global GPS_X
    global GPS_Y
    global IS_AUTO_MODE
    if IS_AUTO_MODE:
        GPS_X.append(localization_data.pose.position.x)
        GPS_Y.append(localization_data.pose.position.y)
        #print localization_data.pose.position.x,localization_data.pose.position.y,len(GPS_X)

def setup_listener():
    rospy.init_node('plot_listener', anonymous=True)
    rospy.Subscriber(CHASSIS_TOPIC, chassis_pb2.Chassis, chassis_callback)
    rospy.Subscriber(LOCALIZATION_TOPIC, localization_pb2.LocalizationEstimate,
                     localization_callback)


def update(frame_number):
    global GPS_X
    global GPS_Y
    if IS_AUTO_MODE and len(GPS_X) > 1:
        min_len = min(len(GPS_X), len(GPS_Y)) - 1
        GPS_LINE.set_data(GPS_X[-min_len:], GPS_Y[-min_len:])


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(
        description=
        """A visualization tool that can plot a manual driving trace produced by the rtk_player tool,
        and plot the autonomous driving trace in real time.
        The manual driving trace is the blue lines, and the autonomous driving trace is the red lines.
        It is visualization a way to verify the precision of the autonomous driving trace.
        If you have a rosbag, you can play the rosbag and the tool will plot the received localization
        message in realtime. To do that, start this tool first with a manual driving trace, and then
        play rosbag use another terminal with the following command [replace your_bag_file.bag to your
        own rosbag file]: rosbag play your_bag_file.bag
        """)
    #parser.add_argument(
     #   "trace",
     #   action='store',
     #   type=str,
     #   help='the manual driving trace produced by rtk_player')

    #args = parser.parse_args()

    fig, ax = plt.subplots()
    plt.xlim(-300-515348,300-515348)
    plt.ylim(-300+3317984,300+3317984)
    #handle = file(args.trace, 'r')
    #trace_data = np.genfromtxt(handle, delimiter=',', names=True)
    #ax.plot(trace_data['x'], trace_data['y'], 'b-', alpha=0.5, linewidth=1)
    #handle.close()
    trace_x = list()
    trace_y = list()
    trace_x = [849300,849310,849320,849330]
    trace_y = [3449600,3449610,3449620,3449630]
    setup_listener()

    #x_min = min(trace_data['x'])
    #x_max = max(trace_data['x'])
    #y_min = min(trace_data['y'])
    #y_max = max(trace_data['y'])

    GPS_LINE, = ax.plot(GPS_X, GPS_Y, 'r', linewidth=3, label="gps")

    ani = animation.FuncAnimation(fig, update, interval=100)
    plt.grid()
    plt.show()
