from datetime import datetime

default_questions = ["What did you work on yesterday?", "What are you planning to work on today?", "Are you blocked on anything?", "When do you think you will be complete current task?"]
class standup:
    def __init__(self):
        self.questions = default_questions
        self.members = []
        self.time = None
        self.days = 0   #124 1111100
        self.reporting_room = None
        self.name = "Standup"
        self.upcoming = None
        self.answers = {}

    def create(self):
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
        for member in self.members:
            self.answers.update({member: self.construct_answer_array(member)})
        print(self.report())

    def construct_answer_array(self, member):
        answers = []
        for question in self.questions:
            print(question)
            answers.append(input())
        return answers

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



