#utils
import random
import re
import json
from time import strftime

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

async def saveQuote(ctx):
    if(ctx.message.reference is None):
        await ctx.channel.send("You must use !quoteThis while replying to a message")
        return
    else:
        message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
        quoteObject = {"author":message.author.id, "content": message.content, "date": message.created_at.strftime("%A, %B %d, %Y")}

        data = readDb()
        quotes = data.get("quotes",0)
        quotes.append(quoteObject)
        data['quotes'] = quotes
        writeDb(data)
        await ctx.channel.send("The following quote has been saved:")
        await ctx.channel.send(message.content + " - <@"+str(message.author.id)+"> " + " written on " + message.created_at.strftime("%A, %B %d, %Y"))

async def randomQuote(message):
    data = readDb()
    quotes = data.get('quotes')
    chosenQuote = random.choice(quotes)
    print(chosenQuote)
    await message.channel.send(chosenQuote['content'] + " - <@"+str(chosenQuote['author'])+"> " + " written on " + chosenQuote['date'])