import app
import os

from scratch2py import Scratch2Py
s2py = Scratch2Py('JethreeH', os.environ.get('PASS'))

app.keep_alive()

with open('data.json', 'r') as file:
    data = json.load(file)

def readCloudVar( projectId , key ):
    cloudProject = s2py.scratchConnect(projectId)
    value = cloudProject.readCloudVar(key)
    return value

def setCloudVar( projectId , key , value):
    cloudProject = s2py.scratchConnect(projectId)
    try :
        cloudProject.setCloudVar(key, value)
        return True
    except:
        return False


while True:
  for project in data:
    if not(readCloudVar(project, 'transferring') == 0):
      # Parse the data
      pass
      
  pass
