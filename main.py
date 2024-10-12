
import os
import helpers
import time
import json
from datetime import datetime , timedelta


from scratch2py import Scratch2Py

s2py = Scratch2Py("JethreeH", 'peppapig30')

master_id = ''

with open("data.json", "r") as file:
    data = json.load(file)




def readCloudVar(projectId, key, connect=True):
    try:
        if connect:
            cloudProject = s2py.scratchConnect(projectId)
        value = cloudProject.readCloudVar(key)
        return value
    except:
        time.sleep(1)
        return readCloudVar(projectId, key)


def setCloudVar(projectId, key, value, connect=True):
    if connect:
        cloudProject = s2py.scratchConnect(projectId)
    try:
        cloudProject.setCloudVar(key, value)
        return True
    except:
        return False


while True:
    old_data = data
    for project in data:

        transferring = int(readCloudVar(project, "transferring"))
        if not (transferring == 0):
            print(transferring)
            cloudProject = s2py.scratchConnect(project)
            # Parse the data
            if transferring == 1:
                en_key = cloudProject.readCloudVar("key")
                en_val = cloudProject.readCloudVar("value")
                print(en_key, en_val)
                key = helpers.decode(en_key)
                val = helpers.decode(en_val)
                print(key, val)
                data[project][key] = val
                cloudProject.setCloudVar('transferring', '0')
                with open("data.json", "w") as file:
                    json.dump(data, file, indent=4)
            if transferring == 2:
                en_key = cloudProject.readCloudVar("key")
                key = helpers.decode(en_key)
                val = data[project][key]
                en_val = helpers.encode(val)
                cloudProject.setCloudVar('value', en_val)
                cloudProject.setCloudVar('transferring', '3')
                now = datetime.now()
                while int(cloudProject.readCloudVar("transferring")) == 3 and datetime.now() <= now + timedelta(minutes=0.25):
                    time.sleep(0.1)
                cloudProject.setCloudVar('transferring', '0')

    if not (data == old_data):
        print('rewrite')
        with open("data.json", "w") as file:
            json.dump(data, file, indent=4)
