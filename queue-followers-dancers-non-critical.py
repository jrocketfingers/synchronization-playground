import time
import logging
import random
from threading import Lock, Semaphore, Thread

logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-10s) %(message)s')

n = 10

followerQueue = Semaphore(0)
leaderQueue = Semaphore(0)


def dance():
    time.sleep(3)

def leader():
    time.sleep(random.randrange(3,7))
    logging.debug("Leader awaiting")

    followerQueue.release() # let them know we're looking for a follower
    leaderQueue.acquire() # leader stands in queue

    logging.debug("Leader found a match")
    dance()

def follower():
    time.sleep(random.randrange(1,3))
    logging.debug("Follower awaiting")

    leaderQueue.release() # let them know we're looking for a leader
    followerQueue.acquire() # follower stands in queue

    logging.debug("Follower dancing")
    dance()


for i in range(n):
    l = Thread(target=leader)
    l.start()

    f = Thread(target=follower)
    f.start()


logging.debug('Waiting for worker to pass')
