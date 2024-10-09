import app
import os
import helpers
import time
import json

from scratch2py import Scratch2Py

s2py = Scratch2Py("JethreeH", os.environ.get("PASS"))

app.keep_alive()

with open("data.json", "r") as file:
    data = json.load(file)

cloudProject = None


def readCloudVar(projectId, key, connect=True):
    if connect:
        cloudProject = s2py.scratchConnect(projectId)
    value = cloudProject.readCloudVar(key)
    return value


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
            cloudProject = s2py.scratchConnect(project)
            # Parse the data
            if transferring == 1:
                en_key = cloudProject.readCloudVar("key")
                en_val = cloudProject.readCloudVar("value")
                key = helpers.decode(en_key)
                val = helpers.decode(en_val)
                data[project].append({key: val})
                cloudProject.setCloudVar('transferring', '0')
            if transferring == 2:
                en_key = cloudProject.readCloudVar("key")
                key = helpers.decode(en_key)
                val = data[project][key]
                en_val = helpers.encode(val)
                cloudProject.setCloudVar('value', en_val)
                cloudProject.setCloudVar('transferring', '3')
                while int(readCloudVar(project, "key", False)) == 3:
                    time.sleep(0.1)

    if not (data == old_data):
        with open("data.json", "w") as file:
            json.dump(data, file, indent=4)
