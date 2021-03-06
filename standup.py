from datetime import datetime, timedelta
from priority_queue import priority_queue
from threading import Condition, Timer
import pickle
from message_unit import message_unit
from collections import defaultdict
from queue import Queue
from standup_config import *
#from utils import fetch_display_name
#from bot_config import auth_header

SAVE_FILE = "save.dat"
subscriptions = {}
standups = priority_queue()


standup_oq = Queue()
condition = Condition()


IDLE = 0
CREATING = 1
CREATED = 2
RUNNING = 3


#call update_standup whenever you change standups queue. This will notify the timer thread waiting on the condition to re-calculate timer.
#manual insert, update_standup()
#update_standup(standup)  will also insert
#delete element standups queue, update_standup()
def update_standup(new_standup=None):
    global  condition
    global standups
    print("update waitig for condition")
    condition.acquire()
    print("update acquired condition")
    if new_standup:
        standups.insert(new_standup)
    with open(SAVE_FILE, "wb") as f:
        for s in standups:
            pickle.dump(s, f)
    condition.notify()
    condition.release()

def add_question(owner, name, question):
    su = _fetch_standup(owner, name)
    if su:
        su.questions.append(question)
        update_standup()
        return "Question added succesfully. Use /viewquestions to see all question."
    else:
        return "You don't have any meeting named "+name

def delete_question(owner, name, qno):
    print("in standups delete question")
    su = _fetch_standup(owner, name)
    if su:
        print(su.questions)
        print(qno-1)
        su.questions.pop(qno-1)
        print("after pop")
        update_standup()
        print("returning")
        return "Question deleted succesfully. Use /viewquestions to see all question."
    else:
        return "You don't have any meeting named "+name

def view_questions(owner, name):
    #print("in view question of standup")
    su = _fetch_standup(owner, name)
    if su:
        res = ""
        index = 1
        for q in su.questions:
            print(q)
            res += str(index) + ". " + q + "\n\n"
            index += 1
        return res
    else:
        return "You don't have any meeting named "+name

def add_default_questions(owner, name):
    #print("in view question of standup")
    su = _fetch_standup(owner, name)
    if su:
      #  print("returning ")
       # print(su.questions)
        su.questions.extend(default_questions)
        update_standup()
        return "Default questions have been added. Please use /viewquestions to check the questions."
    else:
        return "You don't have any meeting named "+name

def add_room(owner, name, room_id):
    su = _fetch_standup(owner, name)
    if su:
        su.reporting_rooms.append(room_id)
        return "Report will be shared in this room."
    return "You don't have any meeting named "+name

def remove_room(owner, name, room_id):
    su = _fetch_standup(owner, name)
    if su:
        if room_id in su.reporting_rooms:
            su.reporting_rooms.remove(room_id)
        else:
            return "This room is not subscribed for meeting "+name
    return "You don't have any meeting named "+name
def add(owner, name, email):
    su = _fetch_standup(owner, name)
    if su:
        su.members[email] = None
        return email + " has been added to " + name
    return "You don't have any meeting named "+name

def delete(owner, name, email):
    su = _fetch_standup(owner, name)
    if su:
        su.members[email] = None
        return email + " has been removed from " + name
    return "You don't have any meeting named "+name



def owned_standups(email, name=None):
    owned = []
    for s in standups:
        if isinstance(s, standup):
            if s.owner == email:
                owned.append(s.name)
    if owned:
        return str(owned)
    return "You don't own any meetings."

def _fetch_standup(owner, name):
    su = None
    for s in standups:
        if isinstance(s, standup):

            if s.owner == owner and s.name == name:
                print("found requested standup")
                su = s
                break
    return su

def delete_standup(owner, name):
    su = _fetch_standup(owner, name)
    if su:
        standups.delete(su)
        update_standup()
        return "Meeting succesfully removed."
    return "No meeting found with given name."

def upcoming_time(owner, name):
    print("getting upcoming")
    su = _fetch_standup(owner, name)
    if su:
       # print(su.upcoming)
        return su.upcoming
    return "No standups found with given name."



def report(owner, name, stp=None):  #name, owner combination will be unique   #TODO should move this more appropriate location     #stp is standup, no need to fetch
    if not stp:
        su = _fetch_standup(owner, name)
        if not su:
            return "No standups found with the given name."
    else:
        su = stp
    answer = "#_"+ su.name + "_ report for the day " + "_" + str(datetime.today().date()) +"_ \n\n ---"
  #  print(su.answers)
    for i in range(len(su.questions)):
        answer += "\n"
        answer += "##"+su.questions[i] +"\n"
        for member in su.answers:
            answer += "\n"+ member
            if i < len(su.answers[member]):
                #answer += "> _"+su.answers[member][i] + "_\n\n"
                answer += ": _" + su.answers[member][i] + "_\n\n"

   # print(su.answers)
    #print(su.members)
    absentees = [m for m in su.members if m not in su.answers]
    print(absentees)
    for a in absentees:
        answer += a + " "
    if absentees:
        answer += " didn't participate in the meeting.\n"
    return answer

def run(owner, name):
    su = _fetch_standup(owner, name)
    if not su:
        return "You don't own any standup with name "+name
    su.run()


def skip_next(owner, name):
    su = _fetch_standup(owner, name)
    if not su:
        return "You don't own any standup with name "+name
    su.upcoming = standup.find_upcoming(su.days, su.time[0], su.time[1], skipnext=True)
    update_standup(su)
    return "Next standup has been postponed to "+ str(su.upcoming)

def validate_name(owner, name):
    print("validating name")
    su = _fetch_standup(owner, name)
    if su:
        print("returning false")
        return False
    return True

def view_meeting(owner, name):
   # print("validating name")
    su = _fetch_standup(owner, name)
    if su:
        return str(su)
    else:
        return "You don't have any meeting named "+ name


class standup():
    def __init__(self, owner):
        #standup_interface.__init__(oq)
        self.questions = []
        self.members = {}
        self.time = None
        self.days = 0   #124 1111100
        self.reporting_rooms = []
        self.name = "Standup"
        self.upcoming = None
       # self.answers = {}
        self.owner = owner
        self.state = IDLE
        self.index = -1
        self.answers = defaultdict(list)


    def update(self, person, text):
        pass

    def process(self, text, person = None):
        if self.state == RUNNING:
            #print("got standup res")
            #print(len(self.answers[person]))
           # print(len(default_questions))
            self.answers[person].append(text)
            if len(self.answers[person]) >= len(self.questions):
                print("got full responses from "+person)
                standup_oq.put(message_unit(None, None, person, "Thank you. :)" ))
                subscriptions.pop(person)
            else:
                print("sending next question.")
                standup_oq.put(message_unit(None, None, person, self.questions[len(self.answers[person])]))

        elif self.state == CREATING:
            if self.index == 0:
                if(validate_name(person, text)):
                    if len(text.split()) != 1:
                        return "Please don't use spaces in name."
                    self.name = text
                else:
                    return "You already have a standup with same name. Please choose another name."
            elif self.index == 1:
                members = list(text.split())
                for member in members:
                    self.members.update({member: None})


            elif self.index == 2:
                week = {'mon': 0, 'tue': 1, 'wed': 2, 'thu': 3, 'fri': 4, 'sat': 5, 'sun': 6}  # TODO validate input
                if text == "week":
                    days = 31 #0011111
                else:
                    days = list(text.lower().split())
                invalid_days = [day for day in days if day not in week]
                if invalid_days:
                    res = "These days are not valid "+ str(invalid_days) + "\n\nPlease enter any of sun, mon, tue, wed, thu, fri, sat."
                    return res
                selected_days = [day for day in week if day in days]
                for day in selected_days:
                    self.days |= 1 << week[day]
            elif self.index == 3:
                try:
                    self.time = tuple(map(int, text.split(":")))   #TODO Validate
                    if self.time[0] > 23 or self.time[1] > 59 or self.time[0] < 0 or self.time[1] < 0:
                        return "Invalid time! Try again."
                except ValueError:
                  #  print("exception")
                    return "Invalid time. Please enter time in HH:MM format."

                self.upcoming = standup.find_upcoming(self.days, self.time[0], self.time[1])

            self.index += 1
            if self.index < len(wizard):
                print("returning ans")
                if self.index == len(wizard) - 1:
                    subscriptions.pop(self.owner)
                   # print("inserting to standups")
                    for m in self.members:
                        standup_oq.put(message_unit(None, None, m, "\n\nHey! You have been added to meeting " + self.name + " by " + self.owner))
                    self.state = CREATED
                    self.index = -1
                    update_standup(self)
                return wizard[self.index]


    def create(self):
        subscriptions.update({self.owner:self})
        self.state = CREATING
        self.index = 0
        return wizard[self.index]

    #days = valid days, day = current day
    @staticmethod
    def get_valid_day(days, day):
        print("get_valid_day " + str(day) + " " + str(days))
        if days > 127 or day > 7:
            return
        s = 0
        while (days & 1 << day) == 0:
          #  print("in while")
            s += 1
            day += 1
            day %= 7
        print("s value " + str(s))
        return s

    @staticmethod
    def find_upcoming(days, h, m, skipnext=None):  #TODO fix skipnext bug
        now = datetime.now()
        if skipnext:
            print("skipnext")
            s = standup.get_valid_day(days, (now.weekday()+1)%7)
        else:
            print("shashank skipnext")
            s = standup.get_valid_day(days, now.weekday())

        if s == 0 and (now.hour < h or (now.hour == h and now.minute < m)):
            print("shashank in if ")
            # valid time for today if today is valid
            upcoming = now.replace(hour=h, minute=m, second=0, microsecond=0)
        else:
            print("shashnk in else")
            if s == 0:
                # time has passed. get next valid day
                s = standup.get_valid_day(days, (now.weekday() + 1) % 7)
                print("s is "+ str(s))
               # s += 1
                print(str(now.day)+" day")
            upcoming = now.replace(day=now.day, hour=h, minute=m, second=0, microsecond=0) #ToDo crash fix day is out of range for month
            upcoming = upcoming + timedelta(days=s)
        return upcoming


    def end_meeting(self):
        print("ending meeting")
        self.state = IDLE
        update_standup()
        for member in subscriptions:     #TODO Shared variable
            standup_oq.put(message_unit(None, None, member, "Thanks you. Meeting has ended."))
        subscriptions.clear()
        su_report = report(None, None, self)
        standup_oq.put(message_unit(None, None, self.owner, su_report))
        for room in self.reporting_rooms:
            standup_oq.put(message_unit(None, room, None, su_report))


    def run(self):
        if not self.questions:
            return
        print("running")
        t = Timer(END_TIME, self.end_meeting)
        t.start()
        self.answers.clear()
        for member in self.members:
            subscriptions.update({member: self})   #TODO synchronize
            self.state = RUNNING
            self.index = 0
            standup_oq.put(message_unit(None, None, member, "Hey! " + "It's time for "+ self.name + "!"))
            standup_oq.put(message_unit(None, None, member, self.questions[self.index]))



    def __str__(self):
        members = ""
        for m in self.members:
            members += m
        time = str(self.time[0]) + ":" + str(self.time[1])
        return "participants: "+ str(members)  +  "\n\n"+ \
                "time: "+ time + "\n\n"\
                "next meeting is at :" + str(self.upcoming)


    def __lt__(self, other):
        return ((self.upcoming - other.upcoming).total_seconds() < 0)

    def __gt__(self, other):
        return not self.__lt__(other)



