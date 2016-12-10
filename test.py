from datetime import datetime
from threading import Timer
x = datetime.today()
y = x.replace(day=x.day+1, hour=1)
print("enter time of the day HH:MM")
t = input()
h,m = map(int, t.split(":"))
print(h)
print(m)

print("enter the days you dont want meeting to run. enter first three letters of days seperated by spcaes. eg sat sun.")
dr = input()
days = 0
dr = dr.lower().split()

week  = {'mon':0, 'tue':1, 'wed':2, 'thu':3, 'fri':4, 'sat':5, 'sun':6}
selected_days = [day for day in week if day not in dr]

for day in selected_days:
    days |= 1 << week[day]

now = datetime.now()

day  = now.weekday()
def get_valid_day(days, day):
    s = 0
    while (days & 1 << day) == 0:
        print("in while")
        s += 1
        day += 1
        day %= 7
    return s
s = get_valid_day(days, now.weekday())
print("s is " + str(s))

if s == 0 and now.hour < h or now.hour == h and now.minute < m:
    print("hey")
    #valid time for today if today is valid
    upcoming = now.replace(hour=h, minute=m, second=0, microsecond=0)
else:
    if s == 0:
        #time has passes. get next valid day
        s = get_valid_day(days, (now.weekday()+1)%7)
        print("hi")
        print(s)
        s += 1
    upcoming = now.replace(day=now.day+s, hour=h, minute=m, second=0, microsecond=0)
print(days)
print(upcoming)

delta_t =  upcoming - datetime.now()
print(delta_t)