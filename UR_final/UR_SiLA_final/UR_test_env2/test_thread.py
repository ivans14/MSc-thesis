import threading
import time


def func1():
    print('thread1')
    time.sleep(1)
    print('t1')

    
def func2():
    print('thread2')
    time.sleep(1)
    print('t2')

# i = 0
threading.Thread(target = func1).start()
print("hello")

# while True:
#     threading.Thread(target = func1).start()
#     threading.Thread(target = func2).start()
