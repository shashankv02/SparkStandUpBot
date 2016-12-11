from datetime import datetime
from priority_queue import priority_queue
from threading import Condition
import pickle
from message_unit import message_unit
from collections import defaultdict
from queue import Queue
SAVE_FILE = "save.dat"
subscriptions = {}
standups = priority_queue()

standup_oq = Queue()
condition = Condition()

def update_standup(new_standup):
    global  condition
    global standups
    print("update waitig for condition")
    condition.acquire()
    print("update acquired condition")
    standups.insert(new_standup)
    with open(SAVE_FILE, "wb") as f:
        for s in standups:
            pickle.dump(s, f)
    condition.notify()
    condition.release()


IDLE = 0
CREATING = 1
CREATED = 2
RUNNING = 3

default_questions = ["What did you work on yesterday?", "What are you planning to work on today?", "Are you blocked on anything?", "When do you think you will be complete current task?"]
wizard = ["Hi, What do you wan to name this meeting?", "Enter emails of participants seperated by spaces.", "Which days do you want to run the standup?", "What time do you want the standup? Enter in HH:MM format.", "Thank you. Meeting has been created succesfully."]


class standup():
    def __init__(self, owner):
        #standup_interface.__init__(oq)

        self.questions = default_questions
        self.members = []
        self.time = None
        self.days = 0   #124 1111100
        self.reporting_room = None
        self.name = "Standup"
        self.upcoming = None
        self.answers = {}
        self.owner = owner
        self.state = IDLE
        self.index = -1
        self.answers = defaultdict(list)


    def update(self, person, text):
        pass

    def process(self, text, person = None):
        if self.state == RUNNING:
            if len(self.answers[person]) >= len(default_questions):
                subscriptions.pop(person)
                print(self.report())
            else:
                self.answers[person].append(text)

        if self.state == CREATING:
            if self.index == 0:
                self.name = text
            elif self.index == 1:
                self.members = list(text.split())
            elif self.index == 2:
                days = list(text.lower().split())
                week = {'mon': 0, 'tue': 1, 'wed': 2, 'thu': 3, 'fri': 4, 'sat': 5, 'sun': 6}
                selected_days = [day for day in week if day in days]
                for day in selected_days:
                    self.days |= 1 << week[day]
            elif self.index == 3:
                try:
                    self.time = tuple(map(int, text.split(":")))
                except ValueError:
                    return "Invalid time. Please enter time in HH:MM format."

                self.upcoming = standup.find_upcoming(self.days, self.time[0], self.time[1])

            self.index += 1
            if self.index < len(wizard):
                print("returning ans")
                if self.index == len(wizard) - 1:
                    subscriptions.pop(self.owner)
                    print("inserting to standups")
                    self.state = CREATED
                    self.index = -1
                    update_standup(self)
                return wizard[self.index]


    def create(self):
        subscriptions.update({self.owner:self})
        self.state = CREATING
        self.index = 0
        return wizard[self.index]


        '''
        print("Hi, What do you wan to name this meeting?")
        self.name = input()

        print("Enter emails of participants seperated by spaces.")
        self.members = list(input().split())

        print("Which days do you want to run the standup?")
        days = list(input().lower().split())

        week = {'mon': 0, 'tue': 1, 'wed': 2, 'thu': 3, 'fri': 4, 'sat': 5, 'sun': 6}
        selected_days = [day for day in week if day in days]
        for day in selected_days:
            self.days |= 1 << week[day]

        print("What time do you want the standup? Enter in HH:MM format.")
        self.time = tuple(map(int, input().split(":")))
        self.upcoming = standup.find_upcoming(self.days, self.time[0], self.time[1])
       # with open(SAVE_FILE, "wb") as f:
        #    pickle.dump(self, f)
        print("Thank you. Succesfully set up your meeting. Next meeting will be on "+self.upcoming)
        '''

    @staticmethod
    def get_valid_day(days, day):
        if days > 127 or day > 7:
            return
        s = 0
        while (days & 1 << day) == 0:
          #  print("in while")
            s += 1
            day += 1
            day %= 7
        return s

    @staticmethod
    def find_upcoming(days, h, m):
        now = datetime.now()
        s = standup.get_valid_day(days, now.weekday())


        if s == 0 and now.hour < h or now.hour == h and now.minute < m:

            # valid time for today if today is valid
            upcoming = now.replace(hour=h, minute=m, second=0, microsecond=0)
        else:
            if s == 0:
                # time has passed. get next valid day
                s = standup.get_valid_day(days, (now.weekday() + 1) % 7)
                s += 1
            upcoming = now.replace(day=now.day + s, hour=h, minute=m, second=0, microsecond=0)
        return upcoming

    def run(self):
        print("running")
        for member in self.members:
            subscriptions.update({member: self})   #TODO synchronize
            self.state = RUNNING
            self.index = 0
            standup_oq.put(message_unit(None, None, member, default_questions[self.index]))


    def report(self):
        for i in range(len(self.questions)):
            print(self.questions[i])
            for member in self.answers:
                print(member)
                print(self.answers[member][i])


    def __str__(self):
        return "participants: "+ str(self.members) + \
                " time: "+ str(self.time) + \
                " name: "+ self.name + \
                " on days: " + str(self.days) + \
                " next meeting is at :" + str(self.upcoming)
        # TODO change self.days from internal repr to days

    def __lt__(self, other):
        return ((self.upcoming - other.upcoming).total_seconds() < 0)

    def __gt__(self, other):
        return not self.__lt__(other)



