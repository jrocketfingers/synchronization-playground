import time
import logging
import random
from threading import Lock, Semaphore, Thread

logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-10s) %(message)s')

mutex = Semaphore(value=1)
turnstile1 = Semaphore(value=0)
turnstile2 = Semaphore(value=0)

n = 10
count = 0

def citizen():
    global count

    for _ in range(10):
        time.sleep(random.randrange(1,5))

        logging.debug("At the barrier.")

        with mutex:
            count += 1
            if count == n:
                logging.debug("Releasing the entry barrier.")
                for _ in range(n):
                    turnstile1.release()

        turnstile1.acquire()

        time.sleep(random.randrange(1,5))

        logging.debug("Past the barrier.")

        # exit
        with mutex:
            count -= 1
            if count == 0:
                logging.debug("Unlocking the exit barrier.")
                for _ in range(n):
                    turnstile2.release() # unlock the exit gate

        turnstile2.acquire()


for i in range(n):
    t = Thread(target=citizen)
    t.start()

logging.debug('Waiting for citiznes to pass')
