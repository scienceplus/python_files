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
Record localization and mobileye lane detection in CSV format
"""

import argparse
import atexit
import logging
import math
import os
import rospy
import sys

from gflags import FLAGS
from std_msgs.msg import String

from logger import Logger
from modules.localization.proto import localization_pb2

global sample_distance 
sample_distance = 0.1

class LaneRecord(object):
    """
    lane recording class
    """

    def write(self, data):
        """wrap file write function to flush data to disk"""
        self.file_handler.write(data)
        self.file_handler.flush()

    def __init__(self, record_file):
        self.firstvalid = False
        self.logger = Logger.get_logger("LaneRecord")
        self.record_file = record_file
        self.logger.info("Record file to: " + record_file)

        self.x_pass = 0
        self.y_pass = 0
        self.lane_width_pass = 0

        try:
            self.file_handler = open(record_file, 'w')
        except:
            self.logger.error("open file %s failed" % (record_file))
            self.file_handler.close()
            sys.exit()

        self.write("x,y,z,theta,dist_l,conf_l,dist_r,conf_r\n")

        self.localization = localization_pb2.LocalizationEstimate()
        self.terminating = False


    def localization_callback(self, data):
        """
        New message received
        """
        if self.terminating == True:
            self.logger.info("terminating when receive localization msg")
            return

        self.localization.CopyFrom(data)
        x = self.localization.gtav.lc_position.x
        y = self.localization.gtav.lc_position.y
        z = self.localization.gtav.lc_position.z
        lane_width = self.localization.gtav.width

        if x != 0 or y != 0:
            if self.x_pass !=0 and self.y_pass !=0:
                if x != self.x_pass:
                    theta = math.atan2(y-self.y_pass,x-self.x_pass)
                #print("self.x_pass,self.y_pass,theta",self.x_pass,self.y_pass,theta)
                #self.write(self.x_pass,self.y_pass,z,theta,dist_l=self.lane_width_pass,conf_l=-1,dist_r=self.lane_width_pass,conf_r=-1 )
                '''                
                self.write(
                    "%s, %s, %s, %s, %s, %s, %s, %s\n" %
                    (self.x_pass, self.y_pass, z, theta, self.lane_width_pass, -1, self.lane_width_pass, -1))
                '''
                self.fill_data(x,y,z,theta,self.x_pass,self.y_pass)
            self.x_pass = x
            self.y_pass = y
            self.lane_width_pass = lane_width/2 -0.2

        '''
        self.write(
            "%s, %s, %s, %s, %s, %s, %s, %s\n" %
            (carx, cary, carz, cartheta, dist_l, conf_l, dist_r, conf_r))
        '''

    def shutdown(self):
        """
        shutdown rosnode
        """
        self.terminating = True
        self.logger.info("Shutting Down...")
        self.logger.info("file is written into %s" % self.record_file)
        self.file_handler.close()
        rospy.sleep(0.1)

    def fill_data(self,x,y,z,theta,x_pass,y_pass):
        global sample_distance
        det_x = x - x_pass
        det_y = y - y_pass
        num_x = det_x / sample_distance
        num_y = det_y / sample_distance
        if num_x > num_y:
            det_y /= num_x 
            while x_pass < x:
                self.write(
                    "%s, %s, %s, %s, %s, %s, %s, %s\n" %
                    (x_pass, y_pass, z, theta, self.lane_width_pass, -1, self.lane_width_pass, -1))
                x_pass += sample_distance
                y_pass += det_y
        else:
            det_x /= num_y
            while y_pass < y:
                self.write(
                    "%s, %s, %s, %s, %s, %s, %s, %s\n" %
                    (x_pass, y_pass, z, theta, self.lane_width_pass, -1, self.lane_width_pass, -1))
                y_pass += sample_distance 
                x_pass += det_x           
                

def main(argv):
    """
    Main rosnode
    """
    rospy.init_node('lane_recorder', anonymous=True)

    parser = argparse.ArgumentParser(
        description='Record Localization and Mobileye Lane Detection in CSV Format')
    parser.add_argument(
        '-d',
        '--dir',
        help='Output and log directory',
        type=str,
        default='/tmp/')
    parser.add_argument(
        '-o',
        '--output_file',
        help='Output CSV file name',
        type=str,
        default='lane.csv')
    args = vars(parser.parse_args())

    log_dir = args['dir']
    record_file = log_dir + "/" + args['output_file']

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    Logger.config(
        log_file=log_dir + "lane_recorder.log",
        use_stdout=True,
        log_level=logging.DEBUG)
    print("runtime log is in %s%s" % (log_dir, "lane_recorder.log"))
    recorder = LaneRecord(record_file)
    atexit.register(recorder.shutdown)

    rospy.Subscriber('/apollo/localization/pose',
                     localization_pb2.LocalizationEstimate,
                     recorder.localization_callback)

    rospy.spin()


if __name__ == '__main__':
    main(sys.argv)
