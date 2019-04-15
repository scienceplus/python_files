#! /usr/bim/env python
# -*- coding: utf-8 -*-
# __author__ * "science +"
# Email: 110@163.com
# a = [0,1,2,3,4,5,6,7,8,9]
# a = [i + 1 for i in range(10)]
# print (a)
# for index,i in enumerate(a):
#     a[index] += 1
# print (a)

# a = map(lambda x:x+1,a)
# # print (a)
# for i in a:print(i)

# a = (i for i in range(10))
# for j in a:
#     print(j)

def A(n):
    count = 0
    while count < n :
        # print(count)
        count = count +1
        yield count

B = A(10)
for i in B:
    print (i)