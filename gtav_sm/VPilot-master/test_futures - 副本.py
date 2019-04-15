#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading, time, signal
import sys
from multiprocessing import Pool
import multiprocessing
PrintA_alive = True
PrintB_alive = True
def printA():
    #global PrintA_alive
    while True:
        print("a")
        time.sleep(1)
        '''
        if not is_exit:
            print ("a")
            time.sleep(1)
        else:
            print("A end")
            PrintA_alive = False
            break
        '''

def printB():
    #global PrintB_alive
    while True:
        print("b")
        time.sleep(1)
        '''
        if not is_exit:
            print ("b")
            time.sleep(1)
        else:
            print("B end")
            PrintB_alive = False
            break
        '''

def quit(signum, frame):
    #global is_exit
    #is_exit = True
    print("You choose to stop me.")
    #sys.exit()

is_exit = False
    
if __name__ == '__main__':

    signal.signal(signal.SIGINT, quit)
    signal.signal(signal.SIGTERM, quit)

    t1 = multiprocessing.Process(target=printA, args=())
    t2 = multiprocessing.Process(target=printB, args=())
    t1.start()
    t2.start()
    print("t1 and t2 start")
    while True:
        print("True")
            
            #if t1.is_alive() or t2.is_alive():
                #print("t1 and t2 isAlive")
            #    pass
        '''
        if not(PrintA_alive and PrintB_alive):
            print(PrintA_alive)
            print(PrintB_alive)
            print("break")
            break
        '''
        
