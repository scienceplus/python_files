#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import time
import threading

from deepgtav.messages import Start, Stop, Dataset, frame2numpy, Scenario, Lanerecord
from deepgtav.client import Client
from deepgtav.control import subscreber_ctrl_cmd



#import cv2

gl_delay_rec = 0.1#100ms

def rec_message(client):
    while True:
        try:
            # We receive a message as a Python dictionary
            message = client.recvMessage()
            #x,y=message["location"]
            if args.record_path != "none":
                for x,y,z in message["location"]:
                    lane_recorde.fill_content(x,y,z)
            # The frame is a numpy array and can be displayed using OpenCV or similar       
            # image = frame2numpy(message['frame'], (320,160))
            # cv2.imshow('img',image)
            # cv2.waitKey(-1)
        except KeyboardInterrupt:
            if args.record_path != "none":
                lane_recorde.close()
            break
        time.sleep(gl_delay_rec)



# Stores a dataset file with data coming from DeepGTAV
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=None)
    parser.add_argument('-l', '--host', default='localhost', help='The IP where DeepGTAV is running')
    parser.add_argument('-p', '--port', default=8000, help='The port where DeepGTAV is running')
    parser.add_argument('-d', '--dataset_path', default='dataset_kong.pz', help='Place to store the dataset')
    parser.add_argument('-r','--record_path',default = 'none',help='record_lane file name')
    args = parser.parse_args()

    # Creates a new connection to DeepGTAV using the specified ip and port. 
    # If desired, a dataset path and compression level can be set to store in memory all the data received in a gziped pickle file.
    #client = Client(ip=args.host, port=args.port, datasetPath=args.dataset_path, compressionLevel=9)
    client = Client(ip=args.host, port=args.port, compressionLevel=9)
    
    # Configures the information that we want DeepGTAV to generate and send to us. 
    # See deepgtav/messages.py to see what options are supported
    #rate = 30 kong
    dataset = Dataset(rate=30, frame=[320,160], throttle=True, brake=True, steering=True, vehicles=True, peds=True, reward=[15.0, 0.0], direction=None, speed=True, yawRate=True, location=True, time=True)
    # Send the Start request to DeepGTAV.
    #kong driveingmode = 786603
    #location=[209,228] traffic light
    scenario = Scenario(location=[2835,3478],drivingMode=[786603,15.0]) # Driving style is set to normal, with a speed of 15.0 mph. All other scenario options are random.
    #scenario = Scenario(drivingMode=[786603,15.0]) # Driving style is set to normal, with a speed of 15.0 mph. All other scenario options are random.
    client.sendMessage(Start(dataset=dataset,scenario=scenario))

    # Start listening for messages coming from DeepGTAV. We do it for 80 hours
    #stoptime = time.time() + 80*3600
    
    if args.record_path != "none":
        lane_recorde = Lanerecord(args.record_path)
    
    # Create threads
    thread_list = []
    thread_list.append(threading.Thread(target=rec_message, name='rec_message_thread',args=(client,)))
    thread_list.append(threading.Thread(target=subscreber_ctrl_cmd, name='subscreber_ctrl_cmd_thread',args=(client,)))
    
    for t in thread_list:
        t.start()
    for t in thread_list:
        t.join()
    

            
    # We tell DeepGTAV to stop
    client.sendMessage(Stop())
    client.close()
