# -*- coding: utf-8 -*-
import qi
import requests
import json
import time
import threading

def getState(baseURL, itemName, auth):
    url = "http://{}/rest/items/{}".format(baseURL, itemName)
    headers = {"Accept": "application/json"}

    try:
        response = requests.get(url, headers=headers, auth=auth)
        response.raise_for_status()
        data = response.json()
        return data.get("state", "UNDEFINED")
    except Exception as e:
        print("[Error] Initial state for {} could not be retrieved:".format(itemName), e)
        return "UNDEFINED"

def sendCommand(baseURL, itemName, command, auth):
    url = "http://{}/rest/items/{}".format(baseURL, itemName)
    headers = {"Content-Type": "text/plain"}

    try:
        response = requests.post(url, headers=headers, auth=auth, data=command)
        if response.status_code == 202:
            print("[sendCommand] {} and {}".format(itemName, command))
        else:
            print("[Error] when sendCommand for {}. Status code:".format(itemName), response.status_code)
            print("Answer:", response.text)
    except Exception as e:
        print("[Connection error] for sendCommand {}:".format(itemName), e)

def postUpdate(baseURL, itemName, state, auth):
    url = "http://{}/rest/items/{}/state".format(baseURL, itemName)
    headers = {"Content-Type": "text/plain"}

    try:
        response = requests.put(url, headers=headers, auth=auth, data=state)
        if response.status_code == 202:
            print("[postUpdate] {} and {}".format(itemName, state))
        else:
            print("[Error] when postUpdate for {}. Status code:".format(itemName), response.status_code)
            print("Answer:", response.text)
    except Exception as e:
        print("[Connection error] for postUpdate {}:".format(itemName), e)

def ItemStateEvent(baseURL, itemName, memory, auth):
    url = "http://{}/rest/events?topics=openhab/items/{}/state".format(baseURL, itemName)
    headers = {"Accept": "text/event-stream"}

    print("[Connect] Start event listener (SSE) for: {}".format(itemName))

    try:
        response = requests.get(url, headers=headers, auth=auth, stream=True)
        for line in response.iter_lines():
            if line.startswith(b"data: "):
                try:
                    payload = json.loads(line[6:])
                    if payload.get("type") == "ItemStateEvent":
                        state = json.loads(payload["payload"])["value"]
                        memory.insertData("{}_status".format(itemName), state)
                        memory.raiseEvent("{}_statusChanged".format(itemName), state)
                        print("[Event] {} and {}".format(itemName, state))
                except Exception as e:
                    print("[Error] when processing event for {}:".format(itemName), e)
    except Exception as e:
        print("[Error] Connection to event stream for {} failed:".format(itemName), e)

def main(session):
    memory = session.service("ALMemory")
    tabletService = session.service("ALTabletService")

    baseURL = "192.168.0.5:8080"
    auth = requests.auth.HTTPBasicAuth("<username>", "<password>")

    # Hier deine Items
    items = {
        "kuecheButton": "iKueche_Hue_Lampen_Schalter",
        "badButton": "iBad_Hue_Lampen_Schalter",
        "iotButton": "iIoT_Hue_Lampen_Schalter",
        "multimediaButton": "iMultimedia_Hue_Lampen_Schalter"
    }

    # Initialzustände setzen
    for buttonId, itemName in items.items():
        initialState = getState(baseURL, itemName, auth)
        memory.insertData("{}_status".format(itemName), initialState)
        print("[Initial] {} and {}".format(itemName, initialState))

    # HTML-UI anzeigen
    htmlFilePath = "http://198.18.0.1/apps/openhab_ui/index2.html"
    tabletService.showWebview(htmlFilePath)

    # Event-Listener für jedes Item starten
    for buttonId, itemName in items.items():
        eventThread = threading.Thread(target=ItemStateEvent, args=(baseURL, itemName, memory, auth))
        eventThread.daemon = True
        eventThread.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        tabletService.hideWebview()
        print("\n[Closed] Display closed.")

if __name__ == "__main__":
    session = qi.Session()
    session.connect("tcp://127.0.0.1:9559")
    main(session)
