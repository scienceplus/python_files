#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import time,signal,sys
from multiprocessing import Process,Queue
import logging
import logging.handlers  
#import multiprocessing
import math
import select
import termios

#from evdev import InputDevice

from deepgtav.messages import Start, Stop, Config,Dataset, frame2numpy, Scenario, Lanerecord,change_position
from deepgtav.client import Client
from topic.localization_sim import gnss_simulation
from topic.chassis_sim import chassis_simulation
from topic.mobileye_sim import mobileye_simulation
from topic.control_sim import subscreber_ctrl_cmd
from topic.control_pad_sim import subscreber_ctrl_pad
from deepgtav.obstacles import get_obstacles



#import cv2

#gl_delay_rec = 0.01#10ms
gl_delay_rec = 0#0ms 交出cpu

def quit(signum, frame):
    print('You choose to stop me.')
    sys.exit()

def process_data(message,q_localization,q_chassis,q_obstacles,q_speed):
    localization_list = []
    chassis_list = []
    obstacle_list = []
    obstacles_object_list = []
    if q_localization.full():
        q_localization.get()
    if q_chassis.full():
        q_chassis.get()
    if q_obstacles.full():
        q_obstacles.get()
    if q_speed.full():
        q_speed.get()
    chassis_list.append(message["throttle"])
    chassis_list.append(message["brake"])
    chassis_list.append(message["steering"])
    #print(message["steering"])
    chassis_list.append(message["location"][0]["speed"])
    q_speed.put(message["location"][0]["speed"])
    #print("chassis:")
    #print(chassis_list)
    #logger.debug("chassis:")
    #logger.debug(chassis_list)
    q_chassis.put(chassis_list)
    #yyz
    #q_gear.put(message["gearposition"][0]["gear"])
    # orientation angular_velocity_vrf euler_angles not provide
    localization_list.extend(message["location"][0]["position"])
    localization_list.extend(message["location"][0]["speedVector"])
    localization_list.extend(message["location"][0]["accVector_t"])
    localization_list.extend(message["location"][0]["angular_velocity"])
    localization_list.extend([message["location"][0]["heading"]])
    localization_list.extend(message["location"][0]["accVector_f"])
    localization_list.extend([message["location"][0]["x"]])
    localization_list.extend([message["location"][0]["y"]])
    localization_list.extend([message["location"][0]["z"]])
    localization_list.extend([message["location"][0]["w"]])
    localization_list.extend([message["location"][0]["roll"]])
    localization_list.extend([message["location"][0]["pitch"]])
    localization_list.extend([message["location"][0]["yaw"]])
    localization_list.extend([message["location"][0]["imu"]])
    localization_list.extend(message["location"][0]["angular_velocity_vrf"])

    localization_list.extend(message["lane_cpoint"])

    #print("angular_velocity_vrf",message["location"][0]["angular_velocity_vrf"])
    #print("speed_vector_f",message["location"][0]["speedVector_vrf"])
    #print("lane_cpoint",message["lane_cpoint"])
    #logger.debug("location:")
    #logger.debug(localization_list)
    #print("position:")
    #print(message["location"][0]['position'])
    #print("heading:")
    #print(message["location"][0]["heading"])
    q_localization.put(localization_list)
    #print("localization_list:")
    #print(localization_list)
    #print("vehicles",message["vehicles"])
    for index in message["peds"]:   #merge obstacles include vehicles and peds
        message["vehicles"].append(index)
    obstacles_object_list = get_obstacles(message["vehicles"],message["location"])
    q_obstacles.put(obstacles_object_list)


def change_scene(client,dataset_para,scenario_para,local_list,scene_list,i):
    
    #fd = sys.stdin.fileno()
    #dev = InputDevice('/dev/input/enent2')
    r = select.select([sys.stdin],[],[],0.01)
    #r = select.select([dev],[],[],0.01)
    rcode = ""
    #print("r",r)
    if len(r[0]) > 0:
        #print("get word:",r[0])
        rcode = sys.stdin.read(1)
        #rcode = dev.read(1)
        print("key word",rcode)
        if rcode == "b":
            scenario_para.location = local_list
            print("trigle b")
            print(scenario_para.location,scenario_para.vehicle,scenario_para.time)
            print(dataset_para.reward,dataset_para.vehicles)
            #client.sendMessage(change_position(dataset=dataset_para,scenario=scenario_para))
            #client.sendMessage(Stop())
            #client.sendMessage(Config(dataset=dataset_para,scenario=scenario_para))
            client.sendMessage(change_position(dataset=dataset_para,scenario=scenario_para))
        elif rcode == "c":
            scenario_para.location = scene_list[i]
            #scenario_para.location = local_list
            print("trigle c")
            print(scenario_para.location,scenario_para.vehicle,scenario_para.time)
            print(dataset_para.reward,dataset_para.vehicles)
            #client.sendMessage(change_position(dataset=dataset_para,scenario=scenario_para))
            client.sendMessage(Config(dataset=dataset_para,scenario=scenario_para))
            i = i+1
            local_list = scenario_para.location
            
    return i,local_list
    
def rec_message(client,lane_recorde,q_localization,q_chassis,q_obstacles,q_speed):
    x_pass = 0
    y_pass = 0
    theta = 0
    z = 0
    while True:
        try:
            # We receive a message as a Python dictionary
            message = client.recvMessage()
            #print("rec_message message")
            #x,y=message["location"]
            if lane_recorde != False:
                pass                
                
                x,y,lane_width = message["lane_cpoint"]
                if x != 0 or y != 0:
                    if x_pass !=0 and y_pass !=0:
                        if x != x_pass:
                            theta = math.atan2(y-y_pass,x-x_pass)
                        #print("x_pass,y_pass,theta",x_pass,y_pass,theta)
                        lane_recorde.fill_content(x_pass,y_pass,z,theta,dist_l=lane_width_pass,conf_l=-1,dist_r=lane_width_pass,conf_r=-1 )

                    x_pass = x
                    y_pass = y
                    lane_width_pass = lane_width/2 -0.2
                
                
                #lane_recorde.fill_content(x,y,z,theta)
            process_data(message,q_localization,q_chassis,q_obstacles,q_speed)
            # The frame is a numpy array and can be displayed using OpenCV or similar       
            # image = frame2numpy(message['frame'], (320,160))
            # cv2.imshow('img',image)
            # cv2.waitKey(-1)
        except KeyboardInterrupt:
            #if record_path != "none":
            #print("file close")
            lane_recorde.close()
            #print("rec_message break")
            break
        time.sleep(gl_delay_rec)



# Stores a dataset file with data coming from DeepGTAV
if __name__ == '__main__':
    scene_list = [[2839.82516184,3480.14707588],[2413.391,3863.607],[-375.194274902,-2105.598632812]]
    parser = argparse.ArgumentParser(description=None)
    parser.add_argument('-l', '--host', default='localhost', help='The IP where DeepGTAV is running')
    parser.add_argument('-p', '--port', default=8000, help='The port where DeepGTAV is running')
    parser.add_argument('-d', '--dataset_path', default='dataset_kong.pz', help='Place to store the dataset')
    parser.add_argument('-r','--record_path',default = 'none',help='record_lane file name')
    #parser.add_argument('-l','--localization',default = [2839.82516184,3480.14707588],help='where the vehicle is')
    parser.add_argument('-x','--loc_x',default = 2839.82516184,help='where the vehicle is')
    parser.add_argument('-y','--loc_y',default = 3480.14707588,help='where the vehicle is')
    args = parser.parse_args()

    local_list = [float(args.loc_x),float(args.loc_y)]
    
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    hdr = logging.StreamHandler()
    formatter = logging.Formatter('[%(asctime)s] %(name)s:%(levelname)s: %(message)s')
    hdr.setFormatter(formatter)
    logger.addHandler(hdr)


    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    new_settings = old_settings
    new_settings[3] = new_settings[3] & ~termios.ICANON
    new_settings[3] = new_settings[3] & ~termios.ECHONL
    #print("old setting %s" %(repr(old_settings)))
    termios.tcsetattr(fd,termios.TCSAFLUSH,new_settings)

    # Creates a new connection to DeepGTAV using the specified ip and port. 
    # If desired, a dataset path and compression level can be set to store in memory all the data received in a gziped pickle file.
    #client = Client(ip=args.host, port=args.port, datasetPath=args.dataset_path, compressionLevel=9)
    #client = Client(ip=args.host, port=args.port, compressionLevel=9)
    client = Client(ip="10.29.1.135", port=args.port, compressionLevel=9)
    
    # Configures the information that we want DeepGTAV to generate and send to us. 
    # See deepgtav/messages.py to see what options are supported
    #rate = 30 kong
    dataset = Dataset(rate=30, frame=[320,160], throttle=True, brake=True, steering=True, vehicles=True, peds=True, reward=[15.0, 0.0], direction=None, speed=True, yawRate=True, location=True, time=True)
    # Send the Start request to DeepGTAV.
    #kong driveingmode = 786603
    #location=[209,228] traffic light
    #location=[2839.82516184,3480.14707588] high speed
    #scenario = Scenario(location=[2839.82516184,3480.14707588],time=[20,30],weather="CLEAR",vehicle="ninef2",drivingMode=[-1,15.0]) # Driving style is set to normal, with a speed of 15.0 mph. All other scenario options are random.
    #print(float(args.loc_x),float(args.loc_y))
    scenario = Scenario(location=local_list,time=[10,30],weather="CLEAR",vehicle="ninef2",drivingMode=[-1,15.0])
    #scenario = Scenario(drivingMode=[786603,15.0]) # Driving style is set to normal, with a speed of 15.0 mph. All other scenario options are random.
    client.sendMessage(Start(dataset=dataset,scenario=scenario))

    # Start listening for messages coming from DeepGTAV. We do it for 80 hours
    #stoptime = time.time() + 80*3600
    
    if args.record_path != "none":
        lane_recorde = Lanerecord(args.record_path)
    else:
	    lane_recorde = False
    
    # Create threads
    '''
    thread_list = []
    thread_list.append(threading.Thread(target=rec_message, name='rec_message_thread',args=(client,)))
    thread_list.append(threading.Thread(target=subscreber_ctrl_cmd, name='subscreber_ctrl_cmd_thread',args=(client,)))
    
    for t in thread_list:
        t.start()
    for t in thread_list:
        t.join()
    '''
    
    '''
    #create processing pool
    ps = Pool(4)
    ps.apply_async(rec_message,args=(client,))
    
    ps.close()
    ps.join()
    '''
    
    try:
        signal.signal(signal.SIGINT, quit)
        signal.signal(signal.SIGTERM, quit)
        q_localization = Queue(2)
        q_chassis = Queue(2)
        q_obstacles = Queue(2)
        q_drivemode = Queue(2)
        q_speed = Queue(2)
        q_drivemode2control = Queue(2)
        q_gear = Queue(2)  #yyz
        a = Process(target=rec_message, args=(client,lane_recorde,q_localization,q_chassis,q_obstacles,q_speed))
        b = Process(target=gnss_simulation, args=(q_localization,))
        c = Process(target=chassis_simulation, args=(q_chassis,q_drivemode,q_gear))
        d = Process(target=mobileye_simulation, args=(q_obstacles,))
        e = Process(target=subscreber_ctrl_cmd, args=(client,q_speed,q_drivemode2control,q_gear))
        f = Process(target=subscreber_ctrl_pad, args=(client,q_drivemode,q_drivemode2control))
        a.start()
        b.start()
        c.start()
        d.start()
        e.start()
        f.start()


        dataset_para = Dataset()
        scenario_para = Scenario()
        local_list_para = local_list
        scene_list_lenth = len(scene_list)
        for j in range(scene_list_lenth):
            if scene_list[j] == local_list:
                i = j+1
        while True:
            if i >= scene_list_lenth:
                i = 0
            i,local_list_para = change_scene(client,dataset,scenario,local_list_para,scene_list,i)
            time.sleep(gl_delay_rec)
            pass
    except Exception as exc:
        print("exc:")
        print(exc)

    print("sendMessage stop")
    # We tell DeepGTAV to stop
    client.sendMessage(Stop())
    client.close()
