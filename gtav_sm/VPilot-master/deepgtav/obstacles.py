#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
'''
gl_ob_Original_id = [43778,5555]
gl_ob_Transfor_id = [0,1]
gl_ob_Or_id_to_Tr_id = {'43778': 0,'5555':1}
'''
gl_ob_Original_id = []
gl_ob_Transfor_id = []
gl_ob_Or_id_to_Tr_id = {}
gl_ob_speed_time = {}
#test
#obstacles = [{'BLL': [-14.995010375976562, -51.958282470703125, -1.17755126953125], 'classID': 0, 'heading': 344.1528625488281, 'time_ms': 316588, 'id': 43778, 'FUR': [-11.752456665039062, -47.916168212890625, 0.1582794189453125], 'speed': 6.447366714477539, 'position': [201.87466430664062, 175.3121795654297, 104.92576599121094]}, {'BLL': [11.908843994140625, -40.19593811035156, -1.2063674926757812], 'classID': 0, 'heading': 70.4248275756836, 'time_ms': 316588, 'id': 67842, 'FUR': [8.200836181640625, -36.53843688964844, 0.10872650146484375], 'speed': 1.0358411073684692, 'position': [225.30323791503906, 186.88221740722656, 104.88658142089844]}, {'BLL': [-21.585678100585938, -56.735809326171875, -1.3129425048828125], 'classID': 0, 'heading': 341.2658386230469, 'time_ms': 316588, 'id': 49410, 'FUR': [-18.196365356445312, -52.89599609375, 0.238006591796875], 'speed': 0.0, 'position': [195.3573760986328, 170.43350219726562, 104.89793395996094]}, {'BLL': [-6.103424072265625, -3.7601165771484375, -0.75592041015625], 'classID': 0, 'heading': 158.52464294433594, 'time_ms': 316588, 'id': 52482, 'FUR': [-9.238555908203125, -6.9260101318359375, 0.7379302978515625], 'speed': 2.5094192028045654, 'position': [207.57740783691406, 219.90634155273438, 105.42640686035156]}, {'BLL': [13.504653930664062, -35.48497009277344, -1.0945358276367188], 'classID': 0, 'heading': 69.54641723632812, 'time_ms': 316588, 'id': 80898, 'FUR': [9.443191528320312, -31.819778442382812, 0.43070220947265625], 'speed': 0.9465325474739075, 'position': [226.72232055664062, 191.59703063964844, 105.10348510742188]}]
#localization = [{'angular_velocity': [-0.0, 0.0, 0.0], 'accVector_f': [9.506408781979559e-42, 9.506408781979559e-42, 9.506408781979559e-42], 'heading': 160.64016723632812, 'accVector_t': [9.506408781979559e-42, 9.506408781979559e-42, 9.506408781979559e-42], 'speed': 0.0, 'position': [215.24839782714844, 225.24940490722656, 105.4354019165039], 'speedVector_vrf': [0.0, 0.0, 0.0], 'speedVector': [0.0, -0.0, 0.0]}]
#test
class Obstacle:
    def __init__(self,id_ob,type_ob,x,y,angle,length,width,acc,rel_vel_x,status):
        self.obstacle_id = id_ob #range 0:63
        self.obstacle_type = type_ob    #range 0:7 0-Vehicle 1-Truck 2-Bike 3-Ped 4-Bicycle 5-Unused
        self.obstacle_x = x
        self.obstacle_y = y
        self.obstacle_angle = angle  #range -327.68:327.68 Unit:degree
        #self.obstacle_speed = speed
        self.obstacle_length = length    #range 0:31 Unite:meter
        self.obstacle_width = width  #range 0:12.5 Unite:meter
        self.obstacle_acc = acc
        self.obstacle_rel_vel_x = rel_vel_x  #Longitudinal relative velocity
        self.obstacle_status = status    #0-undefined 1-standing 2-stopped 3-moving 4-oncoming 5-parked 6-unused
        pass


def get_obstacles(obstacles,localization):
#def get_obstacles():#test
    global gl_ob_Original_id
    global gl_ob_Transfor_id
    global gl_ob_Or_id_to_Tr_id
    global gl_ob_speed_time
    
    #global obstacles    #test
    #global localization #test
    
    list_id = []
    obstacles_list = []
    for index in range(len(obstacles)):
        list_id.append(obstacles[index]["id"])
    #print("list_id",list_id)
    #print(list_id)
    remove_index = []
    for index in range(len(gl_ob_Original_id)):
        if gl_ob_Original_id[index] not in list_id: #Remove the missing obstacle
            remove_index.append(index)
    remove_index.sort(reverse = True)	#reverse sort
    for index in remove_index:
        gl_ob_Transfor_id.remove(gl_ob_Or_id_to_Tr_id[str(gl_ob_Original_id[index])])
        del gl_ob_Or_id_to_Tr_id[str(gl_ob_Original_id[index])]
        del gl_ob_Original_id[index]
            
            #del gl_ob_speed_time[str(gl_ob_Original_id[index])]
    for index in range(len(list_id)):   #Add new obstacles
        if list_id[index] not in gl_ob_Original_id:
            gl_ob_Original_id.append(list_id[index])
            for i in range(64):    #mobileye request the id must range 0:63
                if i not in gl_ob_Transfor_id:
                    gl_ob_Transfor_id.append(i)
                    gl_ob_Or_id_to_Tr_id.update({str(gl_ob_Original_id[-1]):i})
                    break
                    #gl_ob_speed_time.update({str(gl_ob_Original_id[-1]):[]})
    #print("gl_ob_Transfor_id:",gl_ob_Transfor_id)
    #print("gl_ob_Or_id_to_Tr_id:",gl_ob_Or_id_to_Tr_id)
    #print("gl_ob_Original_id:",gl_ob_Original_id)
    #heading_loc = (localization[0]["heading"]*math.pi)/180
    #heading_loc = -localization[0]["yaw"]
    heading_loc = localization[0]["heading"] + 0.5*math.pi
    
    cos_loc = math.cos(heading_loc)
    sin_loc = math.sin(heading_loc)
    for index in range(len(obstacles)):
        '''
        print("speed:")
        print(obstacles[index]["speed"])
        print("time_ms:")
        print(obstacles[index]["time_ms"])
        print("id")
        print(str(obstacles[index]["id"]))
        '''
        #gl_ob_speed_time[str(obstacles[index]["id"])] = []
        #gl_ob_speed_time[str(obstacles[index]["id"])].append(obstacles[index]["speed"])
        #gl_ob_speed_time[str(obstacles[index]["id"])].append(obstacles[index]["time_ms"])
        #print(gl_ob_speed_time)
        #print(index)
        #if len(gl_ob_speed_time.keys()) >= 4:
        #    ob_acc = ((gl_ob_speed_time[str(obstacles[index]["id"])][2] - gl_ob_speed_time[str(obstacles[index]["id"])][0])/
        #    ((gl_ob_speed_time[str(obstacles[index]["id"])][3] - gl_ob_speed_time[str(obstacles[index]["id"])][1])))
        #    print("acc:")
        #    print(ob_acc)
        ob_acc = 0
        #print("gl_ob_Or_id_to_Tr_id:")
        #print(gl_ob_Or_id_to_Tr_id)
        id_ob = gl_ob_Or_id_to_Tr_id[str(obstacles[index]["id"])]
        type_ob = obstacles[index]["classID"]
        #print("ob_position:")
        #print(obstacles[index]["position"])
        #print("localization:")
        #print(localization[0]["position"])
        
        x_par = (obstacles[index]["position"][0] - localization[0]["position"][0])
        y_par = (obstacles[index]["position"][1] - localization[0]["position"][1])
        x = x_par*sin_loc - y_par*cos_loc
        y = x_par*cos_loc + y_par*sin_loc
        '''
        x_par = (obstacles[index]["position"][1] - localization[0]["position"][1])
        y_par = -(obstacles[index]["position"][0] - localization[0]["position"][0])
        #x = obstacles[index]["dim"][0]
        y = (-x_par*sin_loc) + y_par*cos_loc
        x = x_par*cos_loc + y_par*sin_loc
        '''
        #angle = obstacles[index]["heading"] - localization[0]["heading"]
        angle = obstacles[index]["heading"]
        #length = abs(obstacles[index]["FUR"][0] - obstacles[index]["BLL"][0])
        #width = abs(obstacles[index]["FUR"][1] - obstacles[index]["BLL"][1])
        length = obstacles[index]["length_v"]
        width = obstacles[index]["width_v"]
        #rel_vel_x = obstacles[index]["speed"]*math.cos(angle)- localization[0]["speed"]
        rel_vel_x = obstacles[index]["speed"]*math.cos(angle)
        speed = obstacles[index]["speed"]
        if speed == 0:
            status = 2  #2-stop
        else:
            status = 3
        obstacle_object = Obstacle(id_ob,type_ob,x,y,angle,length,width,ob_acc,rel_vel_x,status)
        obstacles_list.append(obstacle_object)
    #print("obstacles_list:")
    #print(obstacles_list)
    return obstacles_list


if __name__ == "__main__":
    get_obstacles()
