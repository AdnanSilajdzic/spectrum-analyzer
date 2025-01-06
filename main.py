import discord
import os
from discord import Intents
import json
from dotenv import load_dotenv

# Load environment variables and json files
load_dotenv()
with open("bad-words.json", "r") as file:
    badWordsArray = json.load(file)
with open("pedo-array.json", "r") as file:
    pedoArray = json.load(file)

def read_db():
    with open('db.json', 'r') as file:
        return json.load(file)

def write_db(data):
    with open('db.json', 'w') as file:
        json.dump(data, file, indent=4)


intents = discord.Intents.all()
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

@client.event
async def on_message(message):
    global last_user  # Use the global variable

    # If message is sent by bot, ignore
    if message.author == client.user:
        return

    # Simple hello greeting
    if message.content.startswith("!hello"):
        await message.channel.send(f"Greetings {message.author.mention}")

    if message.content.startswith("good bot"):
        await message.channel.send("😊")

    # Handle faris pedo event
    for pedo_word in pedoArray:
        if pedo_word in message.content.lower() and str(message.author) == "adnan_silajdzic":
            # Read the current count from db.json
            data = read_db()
            farisPedoCount = data.get("farisPedoCount", 0)

            # Increment the count
            farisPedoCount += 1

            # Update the count in db.json
            data["farisPedoCount"] = farisPedoCount
            write_db(data)

            # Send the updated count to the channel
            await message.channel.send(f"Faris pedo count has been incremented. Current count: {farisPedoCount}")
            break

    # Check if a message contains any bad word
    for bad_word in badWordsArray:
        if bad_word in message.content.lower():
            envyId = "<@253113742273806336>"
            await message.channel.send(f"{envyId} SLURS ARE BEING USED IN CHAT BY {message.author.mention}")
            break

client.run(os.getenv('TOKEN'))