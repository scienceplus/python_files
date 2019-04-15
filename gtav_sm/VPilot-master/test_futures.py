import threading, time,signal
import multiprocessing
import sys



def printA():
    while True:
        print('a')
        time.sleep(1)

def printB():
    while True:
        print('b')
        time.sleep(1)

def quit(signum, frame):
    print('You choose to stop me.')
    #sys.exit()
        
if __name__ == '__main__':
    try:
        signal.signal(signal.SIGINT, quit)
        signal.signal(signal.SIGTERM, quit)
        a = multiprocessing.Process(target=printA, args=())
        b = multiprocessing.Process(target=printB, args=())
        a.start()
        b.start()
        while True:
            pass
    except Exception as exc:
        print(exc)