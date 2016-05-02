import time
import logging
import random
from threading import Lock, Semaphore, Thread

logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-10s) %(message)s')

class Barrier:
    def __init__(self, n):
        self.n = n
        self.count = 0

        self.mutex = Semaphore(value=1)
        self.turnstile1 = Semaphore(value=0)
        self.turnstile2 = Semaphore(value=0)

    def phase1(self):
        with self.mutex:
            self.count += 1
            if self.count == self.n:
                logging.debug("Releasing the entry barrier.")
                for _ in range(self.n):
                    self.turnstile1.release()

        self.turnstile1.acquire()

    def phase2(self):
        with self.mutex:
            self.count -= 1
            if self.count == 1:
                logging.debug("Unlocking the exit barrier.")
                for _ in range(self.n):
                    self.turnstile2.release()

        self.turnstile2.acquire()

    def wait(self):
        logging.debug("At the barrier.")
        self.phase1()
        logging.debug("Past the barrier.")
        self.phase2()

barrier = Barrier(10)

def citizen():
    global barrier

    for _ in range(10):
        time.sleep(random.randrange(1,5))

        barrier.wait()


for i in range(10):
    t = Thread(target=citizen)
    t.start()

logging.debug('Waiting for citiznes to pass')
