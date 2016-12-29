from flask import Flask
from flask import request
import json
from utils import *
from message_unit import message_unit
import bot_config
from multiprocessing import Queue
import threading
import api

channels = {}
app = Flask(__name__)
incoming_q = Queue()
outgoing_q = Queue()

running = False
def new_channel(email, q):
    channels.update({email:q})

'''
def route(mu):
    if mu.person_email in channels:
        channels[mu.person_email].put(mu)
    else:
        cq.put(mu)
'''
@app.route("/", methods=['POST'])
def index():
    print("got message")
    data = request.json
    if data['data']['personEmail'] != bot_config.bot_email:
       # geturl = "https://api.ciscospark.com/v1/messages/{0}".format(data['data']['id'])
        msg_json = sendGET(api.MESSAGES+"/{0}".format(data['data']['id']), bot_config.auth_header)
        msg_dict = json.loads(msg_json)
       # print(msg_dict)
        mu = message_unit(msg_dict.get('text'),msg_dict.get('roomId'), msg_dict.get('personEmail'))
        print("mf 1")
        incoming_q.put(mu)
        #route(mu)
    return 'OK'

#get_team_list_url = "https://api.ciscospark.com/v1/team/memberships?teamId=Y2lzY29zcGFyazovL3VzL1RFQU0vMWI1YzJkMjAtOGVmYi0xMWU2LWE2ZTMtNzE2ZmRlMTc5NDMz"
#team_members = sendGET(get_team_list_url)
#team_dict = json.loads(team_members)
#print(team_dict)
def send():
    while running:
        if not outgoing_q.empty():
            print("mf 4")
            mu = outgoing_q.get()
            if mu.room_id == None:
                print("sending to person. "+mu.person_email+" "+mu.response)
                sendPOST(api.MESSAGES, {"toPersonEmail": mu.person_email, "markdown": mu.response}, bot_config.auth_header)
            else:
                sendPOST(api.MESSAGES, {"roomId": mu.room_id, "markdown": mu.response}, bot_config.auth_header)

def start():
    #app.debug = True
    global running
    running = True
    webook_update = {
        "name": "Meetings",
        "targetUrl": bot_config.target_url
    }
    sendPUT(api.WEBHOOKS + "/" + bot_config.webhook_id, webook_update, bot_config.auth_header)
    send_thread = threading.Thread(target=send, name="send thread")
    send_thread.daemon = True
    send_thread.start()
    app.run()