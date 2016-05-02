import time
import logging
import random
from threading import Lock, Semaphore, Thread

logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-10s) %(message)s')

n = 10

def worker():
    pass

for i in range(n):
    t = Thread(target=worker)
    t.start()

logging.debug('Waiting for workers to finish')
