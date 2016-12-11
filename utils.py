import requests

messages_url = "https://api.ciscospark.com/v1/messages/"

#bearer = 'MTg4YjQ2NWMtMGY5NS00NDY3LWI0N2QtYWQ3MTcwY2U1ODkzYWY3ZDAyNWUtOTM2'
import traceback
def sendGET(url, header):
    #header = {"Content-type": "application/json; charset=utf-8", header}
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
   # header = { "Authorization": "Bearer "+bearer}
    try:
        requests.put(url, data=data, headers=header)

    except Exception as e:
        print(e)
        traceback.print_exc()
        print("sendPUT exception")

