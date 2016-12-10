import standup
import pickle
import threading
from datetime import datetime
from priority_queue import priority_queue

SAVE_FILE = "save.dat"

condition = threading.Condition()

def update_standup(new_standup):
    print("update waitig for condition")
    condition.acquire()
    print("update acquired condition")
    standups.insert(new_standup)
    for s in standups:
        with open(SAVE_FILE, "wb") as f:
            pickle.dump(s, f)
    condition.notify()
    condition.release()


def process(cmd):
    global standups
    if cmd == "/new standup":
        new_standup = standup.standup()
        new_standup.create()
        #with open(SAVE_FILE, "ab") as f:
         #   pickle.dump(new_standup, f)
        update_standup(new_standup)

    if cmd == "show":
        print(len(standups))

    if cmd == "next":
        print(standups.get_min().upcoming)




def timer():
    global condition
    condition.acquire()
    print("acquired")
    while True:
        delta_t = None
        if standups.get_min():
            delta_t = standups.get_min().upcoming - datetime.now()
            if delta_t.total_seconds() < 0:
                current = standups.del_min()
                condition.release()
                worker_thread = threading.Thread(target=current.run)
                worker_thread.daemon = True
                #current.run()
                current.upcoming = standup.standup.find_upcoming(current.days, current.time[0], current.time[1])
                update_standup(current)
                worker_thread.start()
                condition.acquire()
                continue
        print("before wait")
        if delta_t:
            print("in delta_t")
            condition.wait(delta_t.total_seconds())   #releases the lock
        else:
            condition.wait()
        print("notified")


try:
    standups = priority_queue()
    with open(SAVE_FILE, "rb") as savefile:
        while True:
            try:
                standups.insert(pickle.load(savefile))
            except(EOFError):
                break
except FileNotFoundError:
    pass

timer_thread = threading.Thread(target=timer)
timer_thread.daemon = True
timer_thread.start()
while True:
    process(input())