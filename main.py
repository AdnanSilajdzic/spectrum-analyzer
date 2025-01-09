import random
import discord
import os
from discord import Intents
import json
from dotenv import load_dotenv
from utils import readDb, writeDb,findWholeWord, updateUKrevetuCount, updatePedoCount

# Load environment variables and json files
load_dotenv()
with open("bad-words.json", "r") as file:
    badWordsArray = json.load(file)
with open("pedo-array.json", "r") as file:
    pedoArray = json.load(file)
with open("secret-messages.json", "r") as file:
    secretMessages = json.load(file)

intents = discord.Intents.all()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

@client.event
async def on_message(message):

    # If message is sent by bot, ignore
    if message.author == client.user:
        return

    # Simple hello greeting
    if message.content.startswith("!hello"):
        await message.channel.send(f"Greetings {message.author.mention}")

    # Good bot reaction
    if findWholeWord("good bot")(message.content.lower()):
        await message.channel.send("😊")
    
    # U krevetu event
    if findWholeWord("!uKrevetu")(message.content):
        krevetCount = updateUKrevetuCount(message)
        await message.channel.send(f"U krevetu! Counter for user <@{message.author.id}> has increased to {krevetCount}")

    # Handle faris pedo event
    for pedo_word in pedoArray:
        if findWholeWord(pedo_word)(message.content) and str(message.author) == "tickwreck":
            farisPedoCount = updatePedoCount()
            await message.channel.send(f"Faris pedo count has been incremented. Current count: {farisPedoCount}")
            break
    
    if findWholeWord("pro tip")(message.content):
        await message.channel.send(f"<@{message.author.id}> "+secretMessages.get('proTip',0))

    #0.1% chance to bully Faris for no reason whatsoever
    if str(message.author) == "tickwreck":
        percentage_chance = 0.001
        if random.random() < percentage_chance:
            await message.channel.send(f"Get your goofy yahoo ass out of here <@{message.author.id}>")


    # Check if a message contains any bad word
    for bad_word in badWordsArray:
        if findWholeWord(bad_word)(message.content):
            envyId = "<@253113742273806336>"
            await message.channel.send(f"{envyId} SLURS ARE BEING USED IN CHAT BY {message.author.mention}")
            break
    
    # LIST ACTION
    if findWholeWord("!farisPedoCounter")(message.content):
        data = readDb()
        await message.channel.send("The Faris pedo counter is currently at " + str(data.get("farisPedoCount", 0)) + "... so far")
    
    if  findWholeWord("!uKrevetuLeaderboard")(message.content):
        data = readDb()
        for user in data["krevetCounter"]:
            await message.channel.send("<@"+str(user)+"> has a score of "+ str(data["krevetCounter"][user]))
        

client.run(os.getenv('TOKEN'))