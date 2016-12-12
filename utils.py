import requests
import json

messages_url = "https://api.ciscospark.com/v1/messages/"

import traceback
def sendGET(url, header):
    try:
        response = requests.get(url, headers=header)
    except:
        print("sendGET exception")
    return response.text

def sendPOST(url, payload, header):
   # header = {"Authorization": "Bearer " + bearer}
    try:
        requests.post(url, data=payload, headers=header)
    except:
        print("sendPOST exception")

def sendPUT(url, data, header):
    try:
        requests.put(url, data=data, headers=header)

    except Exception as e:
        print(e)
        traceback.print_exc()
        print("sendPUT exception")

def fetch_display_name(email, header):
    response = sendGET("https://api.ciscospark.com/v1/people?email=" + email, header)
    return json.loads(response).get('displayName')



