import standup
import pickle
import threading
from datetime import datetime
import standup



#SAVE_FILE = "save.dat"

#condition = threading.Condition()

iq = None
oq = None



def process(mu):
    cmd = mu.text

    #global standups
    if cmd == "/new standup":
        new_standup = standup.standup(mu.person_email)
       #new_standup.iq.put(mu)
        mu.response = new_standup.create()
        print(mu.response)
        print("mf 3.1")
        oq.put(mu)

    elif cmd == "show":
        mu.response = len(standup.standups)
        print("mf 3")
        oq.put(mu)

    elif cmd == "next":
        next_standup = standup.standups.get_min()
        if next_standup:
            mu.response = standup.standups.get_min().upcoming
        else:
            mu.response = "no upcoming standups."
        oq.put(mu)
    else:
        if mu.person_email in standup.subscriptions:
            mu.response = standup.subscriptions[mu.person_email].process(mu.text)
            oq.put(mu)

def timer(_condition):
   # global condition
    condition = _condition
    condition.acquire()
    print("acquired")
    while True:
        delta_t = None
        if standup.standups.get_min():
            delta_t = standup.standups.get_min().upcoming - datetime.now()
            if delta_t.total_seconds() < 0:
                print("starting standup")
                current = standup.standups.del_min()
                condition.release()
                worker_thread = threading.Thread(target=current.run)
                worker_thread.daemon = True
                #current.run()
                current.upcoming = standup.standup.find_upcoming(current.days, current.time[0], current.time[1])
                standup.update_standup(current)
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

def oq_consumer(q):
    while True:
        if not q.empty():
            oq.put(q.get())

def start(incoming_q, outgoing_q):
    global iq, oq
    iq = incoming_q
    oq = outgoing_q
  #  global standups
    try:
        with open(standup.SAVE_FILE, "rb") as savefile:
            while True:
                try:
                    content = (pickle.load(savefile))
                    if isinstance(content, standup.standup):
                        print(content)
                        standup.standups.insert(content)
                except(EOFError):
                    break
    except FileNotFoundError:
        pass

    timer_thread = threading.Thread(target=timer, args=(standup.condition,))
    timer_thread.daemon = True
    timer_thread.start()

    oq_thread = threading.Thread(target=oq_consumer, args=(standup.standup_oq,))
    oq_thread.daemon = True
    oq_thread.start()
    while True:
        while not iq.empty():
            print("mf 2")
            process(iq.get())