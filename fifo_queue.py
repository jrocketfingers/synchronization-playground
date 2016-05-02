import time
import logging
import random
from collections import deque
from threading import Lock, Semaphore, Thread

logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-10s) %(message)s')

n = 10

class FifoQueue:
    def __init__(self, n):
        self.n = n
        self.queue = deque(maxlen=n)

    def wait(self):
        sem = Semaphore(0)
        self.queue.append(sem)
        sem.acquire()

    def signal(self):
        sem = self.queue.popleft()
        sem.release()

q = FifoQueue(n)

def worker():
    global q

    time.sleep(random.randrange(1,3))
    logging.debug("Coming in")
    q.wait()
    logging.debug("Coming out")


for i in range(n):
    t = Thread(target=worker)
    t.start()

for _ in range(n):
    time.sleep(random.randrange(1,3))
    q.signal()

logging.debug('Waiting for workers to finish')
