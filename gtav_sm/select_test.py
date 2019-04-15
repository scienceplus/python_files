import select
import sys
import time
import os
import termios

def kbhit():
    fd = sys.stdin.fileno()
    r = select.select([sys.stdin],[],[],0.01)
    rcode = ""
    if len(r[0]) > 0:
        print('r0',r[0])
        rcode = sys.stdin.read(1)
    return rcode

'''
fd = sys.stdin.fileno()
old_settings = termios.tcgetattr(fd)
new_settings = old_settings
new_settings[3] = new_settings[3] & ~termios.ICANON
new_settings[3] = new_settings[3] & ~termios.ECHONL
print("old setting %s" %(repr(old_settings)))
termios.tcsetattr(fd,termios.TCSAFLUSH,new_settings)
'''
while True:
    c = kbhit()
    if len(c) !=0:
        print("K    %s"%(c))
    else:
        print("Sleep 1")
        time.sleep(1)
