#! /usr/bim/env python
# -*- coding: utf-8 -*-
# __author__ * "science +"
# Email: 110@163.com

def fib(max):
    n, a, b = 0, 0, 1
    while n < max:
        # print(b)
        yield b
        a,b = b,a+b
        n = n+1
    return 'done'
f = fib(10)

for i in f:
    print (i)