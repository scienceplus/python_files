#!/usr/bin/env python
# -*- coding: utf-8 -*-

#import rospy
from cyber_py import cyber
import time

from modules.control.proto import control_cmd_pb2
from deepgtav.messages import Commands

q_d2c = 2   #0:stop 1:start 2:reset
gear_p = 0  #0:N 1:D 2:R

class control_obj:
    def __init__(self,client_obj,q_speed,q_drivemode2control,q_gear):
        self.client = client_obj
        self.q_speed = q_speed
        self.q_d2c = q_drivemode2control
        self.gear = q_gear
    def sim_control_callback(self,ControlCommand_pb):
        global q_d2c,gear_p
        while self.q_speed.empty():
            return
        if not self.q_d2c.empty():
            q_d2c = self.q_d2c.get()
        if q_d2c == 2:
            self.send_message(0,0,0)    #stop
            return
        speed = self.q_speed.get()
        gear_p = ControlCommand_pb.gear_position      #yyz test
        throttle = ControlCommand_pb.throttle/100   #transform to range [0,1]
        brake = ControlCommand_pb.brake/100         #transform to range [0,1]
        #if ControlCommand_pb.steering_target == "nan" or brake == 0.5:
        #    return
        steering_target = ControlCommand_pb.steering_target/100     #transform to range [-1,1]
        
        if speed <= 0.5 and brake > 0:
            throttle = 0
            brake = 0
            steering_target = 0
        
        #print("control_sim:throttle:%f\n,brake:%f\n,steer:%f\n"%(ControlCommand_pb.throttle,ControlCommand_pb.brake,ControlCommand_pb.steering_target))
        #throttle = 0
        #brake = 1
	#steering_target = 0.9
        if steering_target >= 0:
            steering_flag = 0
        else:
            steering_flag = 1
        steering_target = self.steering_table(abs(steering_target))
        if steering_flag == 1:
            steering_target = -steering_target
        '''
        print("time:",ControlCommand_pb.header.timestamp_sec)
        print("throttle:",throttle)
        print("brake:",brake)
        print("steering:",steering_target)
        print("speed",speed)
        '''
        if brake >0.3 and brake <0.4:#test
		brake = 0
                print("brake = 0",throttle ,brake)
        print("throttle brake:",throttle ,brake)
        steering_target = -steering_target
        throttle, brake= gear_position(gear_p,throttle,brake)
        self.send_message(throttle,brake,steering_target)
    def gear_position(self,gear_p,throttle,brake):
        #N
        if gear_p == 0:
            throttle_p = 0
            brake_p = 0
        elif gear_p == 1:
            throttle_p = throttle
            brake_p = brake
        elif gear_p == 2:
            throttle_p = brake
            brake_p = throttle
        return (throttle_p,brake_p)

        # for case in switch(gear_p):
        #     if case('0'):
        #         throttle = 0
        #         brake = 0
        #     if case('1'): pass
        #     if case('2'): pass
    def send_message(self,throttle,brake,steering,gear):
        self.client.sendMessage(Commands(throttle,brake,steering,gear)) #yyz
        pass
    def steering_table(self,steering):
        if steering < 0.000733:
            return 0.2
        elif steering >=0.000733 and steering <0.0733:
            #steering_para = ((steering - 0.000733)/(0.0733 - 0.000733))*(0.3 - 0.2505)+0.2505
            return self.calculate(steering,0.000733,0.0733,0.2505,0.3)
        elif steering >=0.0733 and steering <0.21999:
            return self.calculate(steering,0.0733,0.21999,0.3,0.4)
        elif steering >=0.21999 and steering <0.366:
            return self.calculate(steering,0.21999,0.366,0.4,0.5)
        elif steering >=0.366 and steering <0.51333:
            return self.calculate(steering,0.366,0.51333,0.5,0.6)
        elif steering >=0.51333 and steering <0.65999:
            return self.calculate(steering,0.51333,0.65999,0.6,0.7)
        elif steering >=0.65999 and steering <0.80666:
            return self.calculate(steering,0.65999,0.80666,0.7,0.8)
        elif steering >=0.80666 and steering <0.95333:
            return self.calculate(steering,0.80666,0.95333,0.8,0.9)
        elif steering >=0.95333 and steering <1.0999:
            return self.calculate(steering,0.95333,1.0999,0.9,1.0)
    def calculate(self,steering,low_data_s,high_data_s,low_data_t,high_data_t):
        steering_para = ((steering - low_data_s)/(high_data_s - low_data_s))*(high_data_t - low_data_t)+low_data_t
        return steering_para

def subscreber_ctrl_cmd(client,q_speed,q_drivemode2control,q_gear):
    cyber.init()
    control = control_obj(client,q_speed,q_drivemode2control,q_gear)
    #rospy.init_node('simulation_control', anonymous=True)
    node = cyber.Node("simulation_control")
    
    #rospy.Subscriber('/apollo/control', control_cmd_pb2.ControlCommand,
    #                 control.sim_control_callback)
    node.create_reader('/apollo/control',
                       control_cmd_pb2.ControlCommand,
                       control.sim_control_callback)   
    
    #rospy.spin()
    node.spin()
    #while not cyber.is_shutdown():
    #    time.sleep(0.002)
    
'''
if __name__ == '__main__':
    main(sys.argv)
    
'''
