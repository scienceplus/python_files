#!/usr/bin/env python
# -*- coding: utf-8 -*-

#import rospy
from cyber_py import cyber
import time

from modules.control.proto import pad_msg_pb2
from deepgtav.messages import Commands

class control_pad:
    def __init__(self,client_obj,q_drivemode,q_drivemode2control):
        self.q = q_drivemode
        self.client = client_obj
        self.q_d2c = q_drivemode2control
    def sim_control_pad_callback(self,control_pad_pb):
        if self.q.full():
            self.q.get()
        if self.q_d2c.full():
            self.q_d2c.get()
        drive_mode = control_pad_pb.action
        self.q.put(drive_mode)
        self.q_d2c.put(drive_mode)
        '''
        if drive_mode == 2:	#0:stop 1:start 2:reset
            for i in range(4):
                self.send_message(0,0,0)
                time.sleep(0.5)
        '''
                
    def send_message(self,throttle,brake,steering):
        self.client.sendMessage(Commands(throttle,brake,steering))
        pass

def subscreber_ctrl_pad(client,q_drivemode,q_drivemode2control):
    cyber.init()
    pad = control_pad(client,q_drivemode,q_drivemode2control)
    #rospy.init_node('simulation_control_pad', anonymous=True)
    node = cyber.Node("simulation_control_pad")
    
    #rospy.Subscriber('/apollo/control/pad', pad_msg_pb2.PadMessage,
    #                 pad.sim_control_pad_callback)
    node.create_reader('/apollo/control/pad',
                       pad_msg_pb2.PadMessage,
                       pad.sim_control_pad_callback)    
    #rospy.spin()
    node.spin()
    #while not cyber.is_shutdown():
    #    time.sleep(0.002)
    
'''
if __name__ == '__main__':
    main(sys.argv)
    
'''
