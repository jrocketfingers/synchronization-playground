import time
import logging
import random
from threading import Lock, Semaphore, Thread

logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-10s) %(message)s')

n = 10

leaders = followers = 0
dancefloor = Lock()
followerQueue = Semaphore(0)
leaderQueue = Semaphore(0)


def dance():
    time.sleep(3)

def leader():
    global leaders
    global followers

    time.sleep(random.randrange(3,7))
    logging.debug("Leader awaiting")

    dancefloor.acquire()
    logging.debug("Leader in queue")
    if followers > 0:
        followers -= 1
        followerQueue.release() # let them know we're looking for a follower
    else:
        leaders += 1
        dancefloor.release()
        leaderQueue.acquire() # leader stands in queue

    logging.debug("Leader found a match")
    dance()

    dancefloor.release() # only one od them releases the shared resource


def follower():
    global followers
    global leaders

    time.sleep(random.randrange(1,3))
    logging.debug("Follower awaiting")

    dancefloor.acquire()
    if leaders > 0:
        leaders -= 1
        leaderQueue.release() # let them know we're looking for a leader
    else:
        followers += 1
        logging.debug("Follower - no leaders available")
        dancefloor.release()

        followerQueue.acquire() # follower stands in queue

    logging.debug("Follower dancing")
    dance()


for i in range(n):
    l = Thread(target=leader)
    l.start()

    f = Thread(target=follower)
    f.start()


logging.debug('Waiting for worker to pass')
