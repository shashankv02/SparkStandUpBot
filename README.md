# Spark Stand Up Bot

This is a Bot for Cisco Spark platform that automates daily stadup meetings. The bot contacts your team members whatever time you want to, 
collects work updates, makes a neat report and sends it over to you or shares in a team room.

Just follow a simple wizard to create new meeting and you are done. 


##Creating Standup:

Send /newstandup to the bot. You will be asked the following questions.

**Bot: What do you want to name this meeting?**

You: Titan_Scrum_Standup

**Bot: Enter emails of participants seperated by spaces.**

You: sha@kerbal.com  vin@kerbal.com

**Bot: Which days do you want to run the standup?**

You: mon tue wed 

**Bot: What time do you want the standup? Enter in HH:MM format.**

You: 14:30


**Bot: Thank you. Meeting has been created succesfully.**



sha and vin will be contacted at 2:30PM every monday, tuesday, wednesday and will asked the questions as in following sample standup.



##Standup
**Bot: Hey! It's time for standup.
     What did you work on yesterday?**
     
vin: I've created new presentations for today's client demonstration.

**Bot: What are you planning to work on today?**

vin: I'll be fixing the pending bugs in UI code.

**Bot: Are you blocked on anything?**

vin: No

**Bot: When do you think you will be able complete current task?**

vin: Probably by tomorrow. 

**Bot: Thank you. :)**



A neat formatted report will be sent to scrum master/manager and will also be shared in any room if configured after the meeting has ended. 


##Report
##What did you work on yesterday?##
>vin: I've created new presentations for today's client demonstration.

>sha: I've worked on the call flows.

##What are you planning to work on today?##
>vin: I'll be fixing the pending bugs in UI code.

>sha: I'll continue the same task as yesterday's.

##Are you blocked on anything?##
>vin: No

>sha: I may need some help from call flow expert.

##When do you think you will be able complete current task?##
>vin: Probably by tomorrow.

>sha: Hopefully 2 more days.


##Commands

Following commands are currently supported.

                  /help - get supported commands
                  /newstandup - create a new standup
                  /owned - see standups created by you
                  /report 'standup name' - see report
                  /run 'standup name - run the standup manually
                  /when 'standup name' - show next scheduled time for automated standup
                  /cancel 'standup name' - delete standup 
                  /skipnext 'standup name' - skip next scheduled standup
                  /addroom 'standup name' - report will be shared in the room
                  /removeroom 'standup name' - stop sharing report in the room
                  /add 'standupname' 'email' - add new participant to standup
                  /delete 'standupname' 'email' - delete participant from standup


