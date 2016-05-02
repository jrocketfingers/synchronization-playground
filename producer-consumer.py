import time
import logging
import random
from threading import Lock, Semaphore, Thread
from collections import deque

logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-10s) %(message)s')

n = 10
buffer = deque(maxlen=5)
space = Semaphore(5)
items = Semaphore(0)


def producer():
    for i in range(20):
        event_data = 1 # random.randrange(1, 1)
        time.sleep(event_data) # just use the same value for sleep, is not related

        space.acquire()
        buffer.append(event_data)
        logging.debug('Producer %s; Queue %s' % (i, len(buffer),))
        items.release()

def consumer():
    for i in range(20):
        time.sleep(random.randrange(4, 10))

        items.acquire()
        data = buffer.popleft()
        logging.debug('Consuming %s; Queue %s' % (i, len(buffer),))
        space.release()


p = Thread(target=producer)
p.start()

c = Thread(target=consumer)
c.start()

logging.debug('Waiting for workers to finish')

