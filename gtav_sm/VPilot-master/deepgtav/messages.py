#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import numpy as np
from numpy.lib.stride_tricks import as_strided

class Lanerecord:
    def __init__(self,record_file):
        try:
            self.file_handler = open(record_file,'w',buffering=1)
        except:
            print("open file %s failed"%(record_file))
            self.file_handler.close()
    def write(self,data):
        #print("messages.py",data)
        self.file_handler.write(data)
    def fill_content(self,x,y,z=0,theta=0,dist_l=3,conf_l=0,dist_r=3,conf_r=0):
        #print("messages here")
        self.write("%s, %s, %s, %s, %s, %s, %s, %s\n" %(x,y,z,theta,dist_l,conf_l,dist_r,conf_r))
    def close(self):
        self.file_handler.close()
class Scenario:
    def __init__(self, location=None, time=None, weather=None, vehicle=None, drivingMode=None):
        self.location = location #[x,y]
        self.time = time #[hour, minute]
        self.weather = weather #string
        self.vehicle = vehicle #string
        self.drivingMode = drivingMode #[drivingMode, setSpeed]

class Dataset:
    def __init__(self, rate=None, frame=None, vehicles=None, peds=None, trafficSigns=None, direction=None, reward=None, 
            throttle=None, brake=None, steering=None, speed=None, yawRate=None, drivingMode=None, location=None, time=None):
        self.rate = rate #Hz
        self.frame = frame #[width, height]
        self.vehicles = vehicles #boolean
        self.peds = peds #boolean
        self.trafficSigns = trafficSigns #boolean
        self.direction = direction #[x,y,z]
        self.reward = reward #[id, p1, p2]
        self.throttle = throttle #boolean
        self.brake = brake #boolean
        self.steering = steering #boolean
        self.speed = speed #boolean
        self.yawRate = yawRate #boolean
        self.drivingMode = drivingMode #boolean
        self.location = location #boolean
        self.time = time #boolean

class Start:
    def __init__(self, scenario=None, dataset=None):
        self.scenario = scenario
        self.dataset = dataset

    def to_json(self):
        _scenario = None
        _dataset = None

        if (self.scenario != None):
            _scenario = self.scenario.__dict__

        if (self.dataset != None):
            _dataset = self.dataset.__dict__            

        return json.dumps({'start':{'scenario': _scenario, 'dataset': _dataset}})


class Config:
    def __init__(self, scenario=None, dataset=None):
        self.scenario = scenario
        self.dataset = dataset

    def to_json(self):
        _scenario = None
        _dataset = None

        if (self.scenario != None):
            _scenario = self.scenario.__dict__

        if (self.dataset != None):
            _dataset = self.dataset.__dict__            

        return json.dumps({'config':{'scenario': _scenario, 'dataset': _dataset}})

class change_position:
    def __init__(self, scenario=None, dataset=None):
        self.scenario = scenario
        self.dataset = dataset

    def to_json(self):
        _scenario = None
        _dataset = None

        if (self.scenario != None):
            _scenario = self.scenario.__dict__

        if (self.dataset != None):
            _dataset = self.dataset.__dict__            

        return json.dumps({'change_position':{'scenario': _scenario, 'dataset': _dataset}})

class Stop:
    def to_json(self):
        return json.dumps({'stop':None}) #super dummy

class Commands:
    def __init__(self, throttle=None, brake=None, steering=None):
        self.throttle = throttle #float (0,1)
        self.brake = brake #float (0,1)
        self.steering = steering #float (-1,1)

    def to_json(self):
        return json.dumps({'commands':self.__dict__})
        
def frame2numpy(frame, frameSize):
    buff = np.fromstring(frame, dtype='uint8')
    # Scanlines are aligned to 4 bytes in Windows bitmaps
    strideWidth = int((frameSize[0] * 3 + 3) / 4) * 4
    # Return a copy because custom strides are not supported by OpenCV.
    return as_strided(buff, strides=(strideWidth, 3, 1), shape=(frameSize[1], frameSize[0], 3)).copy()

