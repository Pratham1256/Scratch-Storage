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
            # Parse the data
            if transferring == 1:
                en_key = readCloudVar(project, "key", False)
                en_val = readCloudVar(project, "value", False)
                key = helpers.decode(en_key)
                val = helpers.decode(en_val)
                data[project].append({key: val})
                setCloudVar("transferring", "0", False)
            if transferring == 2:
                en_key = readCloudVar(project, "key", False)
                key = helpers.decode(en_key)
                val = data[project][key]
                en_val = helpers.encode(val)
                setCloudVar("value", en_val, False)
                setCloudVar("transferring", "3", False)
                while int(readCloudVar(project, "key", False)) == 3:
                    time.sleep(0.1)

    if not (data == old_data):
        with open("data.json", "w") as file:
            json.dump(data, file, indent=4)
