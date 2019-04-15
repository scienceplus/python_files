#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import time
import threading
from multiprocessing import Pool
import logging
import logging.handlers  
import os
import signal
import sys
import multiprocessing

#LOG_FILE = r'c:\\Users\201804785\Desktop\GTA5\VPilot-master\test1.log'
#LOG_FILE = r'test1.log'

# 使用一个名字为fib的logger
logger = logging.getLogger('test1')

# 设置logger的level为DEBUG
logger.setLevel(logging.DEBUG)

# 创建一个输出日志到控制台的StreamHandler
hdr = logging.StreamHandler()
#hdr = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=1024 * 1024, backupCount=5, encoding='utf-8')
formatter = logging.Formatter('[%(asctime)s] %(name)s:%(levelname)s: %(message)s')
hdr.setFormatter(formatter)

# 给logger添加上handler
logger.addHandler(hdr)


def CtrlC():
    s1 = "stop"
    logger.debug("ctrl+c%s"%s1)
    #os._exit(0)
    sys.exit(0)

def fun1(msg):
    while True:
        #print("fun1_%s"%msg)
        logger.debug("fun1_%s"%msg)

        time.sleep(0.05)
    #return "done"+msg
def fun2(j):
    #print("fun2_%s"%j)
    #logger.debug("fun2_%s"%j)
    thread_list = []
    thread_list.append(threading.Thread(target=sub_fun1,args=(1,)))
    thread_list.append(threading.Thread(target=sub_fun2,args=(2,)))
    
    for t in thread_list:
        t.setDaemon(True)
        t.start()
    for t in thread_list:
        t.join()
    print("fun2 end")

def sub_fun1(num):
    while True:
        #print("sub_fun1")
        #logger.debug("sub_fun1")
        time.sleep(0.05)
        
def sub_fun2(num):
    while True:
        #print("sub_fun2")
        #logger.debug("sub_fun2")
        time.sleep(0.05)





# Stores a dataset file with data coming from DeepGTAV
if __name__ == '__main__':

    try:
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
        signal.signal(signal.SIGINT, CtrlC)
        signal.signal(signal.SIGTERM, CtrlC)
        #create processing pool
        #ps = Pool(4)
        #result = []
        #ps.apply_async(fun1,("1",))
        #ps.apply_async(fun2,("2",))
        #ps.apply_async(fun1,("1",))
        #ps.close()
        #ps.join()

        
        t1 = multiprocessing.Process(target=fun1, args=("1",))
        t2 = multiprocessing.Process(target=fun2, args=("2",))
        t1.start()
        t2.start()
        t1.join()
        t2.join()
    
        while True:
            pass
    except Exception as e:
        logger.debug(e)
    
    '''
    for i in range(10):
        msg = ("hello %d" %(i))
        print(msg)
        result.append(ps.apply_async(fun1,(msg,)))
    '''
    
    
    '''
    for res in result:
        print (res.get())
    '''
    #fun2(2)
    print("done")
    


