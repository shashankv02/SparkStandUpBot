from flask import Flask
from flask import request
import json
from utils import *
from message_unit import message_unit
from bot_config import *


app = Flask(__name__)



webook_update = {
        "name": "Meetings",
        "targetUrl": target_url
    }
sendPUT(webhook_url+"/"+webhook_id, webook_update)

@app.route("/", methods=['POST'])
def index():
    print("got message")
    data = request.json
    sender = data['data']['personEmail']
    if sender != bot_email:
        geturl = "https://api.ciscospark.com/v1/messages/{0}".format(data['data']['id'])
        msg_json = sendGET(geturl)
        msg_dict = json.loads(msg_json)
        mu = message_unit(msg_dict.get('text'),msg_dict.get('roomId'))

get_team_list_url = "https://api.ciscospark.com/v1/team/memberships?teamId=Y2lzY29zcGFyazovL3VzL1RFQU0vMWI1YzJkMjAtOGVmYi0xMWU2LWE2ZTMtNzE2ZmRlMTc5NDMz"
team_members = sendGET(get_team_list_url)
team_dict = json.loads(team_members)
print(team_dict)


if __name__ == "__main__":
    #app.debug = True
    app.run()