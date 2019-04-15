#! /usr/bim/env python
# -*- coding: utf-8 -*-
# __author__ * "science +"
# Email: 110@163.com

import time
def consumer(name):
    print("%s 准备吃包子啦！"  %name)
    while True:
        baozi = yield
        #TODO
        print ("包子[%s]来了，被[%s]吃了！" %(baozi,name))


def producer(name):
    c = consumer('A')
    c2 = consumer('B')
    c.next()
    c2.next()
    print ("老子开始做包子了！")
    for i in range(5):
        time.sleep(1)
        print ("做了2个包子！")
        c.send(i)
        c2.send(i)
producer("alex")