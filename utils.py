import requests

messages_url = "https://api.ciscospark.com/v1/messages/"

bearer = 'MTg4YjQ2NWMtMGY5NS00NDY3LWI0N2QtYWQ3MTcwY2U1ODkzYWY3ZDAyNWUtOTM2'
def sendGET(url):
    header = {"Content-type": "application/json; charset=utf-8", "Authorization": "Bearer "+bearer}
    try:
        response = requests.get(url, headers=header)
    except:
        print("sendGET exception")
    return response.text

def sendPOST(url, payload):
    header = {"Authorization": "Bearer " + bearer}
    try:
        requests.post(url, data=payload, headers=header)
    except:
        print("sendPOST exception")

def sendPUT(url, data):
    header = { "Authorization": "Bearer "+bearer}
    try:
        response = requests.put(url, data=data, headers=header)
    except:
        print("sendPUT exception")
    print(response.status_code)
    print(response.content)
