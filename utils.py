#utils
import re
import json

def findWholeWord(w):
    return re.compile(r'(?:\W|^){0}(?:\W|$)'.format(re.escape(w)), flags=re.IGNORECASE).search

def readDb():
    with open('db.json', 'r') as file:
        return json.load(file)
    
def writeDb(data):
    with open('db.json', 'w') as file:
        json.dump(data, file, indent=4)

def updateUKrevetuCount(message):
    data = readDb()
    # Ensure 'krevetCounter' exists as a dictionary in the data
    if "krevetCounter" not in data:
        data["krevetCounter"] = {}

    # Get the user's current counter or initialize to 0 if not set
    user_krevet_key = str(message.author.id)
    krevetCount = data["krevetCounter"].get(user_krevet_key, 0)

    # Increment the counter
    krevetCount += 1
    data["krevetCounter"][user_krevet_key] = krevetCount

    # Write the updated data to the database
    writeDb(data)

    # Send the updated counter value
    return krevetCount

def updatePedoCount():
    data = readDb()
    farisPedoCount = data.get("farisPedoCount", 0)

    # Increment the count
    farisPedoCount += 1

    # Update the count in db.json
    data["farisPedoCount"] = farisPedoCount
    writeDb(data)
    return farisPedoCount