import discord
import os
from discord import Intents
import json
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()
with open("bad-words.json", "r") as file:
    badWordsArray = json.load(file)

intents = discord.Intents.all()
client = discord.Client(intents=intents)

# Dictionary to track streaks
user_streaks = {}
last_user = None  # Use None instead of an empty string for clarity

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

    # Handle specific words
    if ("pedophile" in message.content.lower() or "pedo" in message.content.lower() or "pdf file" in message.content.lower()) and \
       message.author != client.user and str(message.author) == "tickwreck":
        await message.channel.send("Faris is calling someone a pedo again")

    # Check if a message contains any bad word
    for bad_word in badWordsArray:
        if bad_word in message.content.lower():
            envyId = "<@253113742273806336>"
            await message.channel.send(f"{envyId} SLURS ARE BEING USED IN CHAT BY {message.author.mention}")
            break

    # Handle YAP streak
    user_id = message.author.id  # Use user ID as the key for the streaks dictionary
    if last_user == user_id:
        # Increment the user's streak
        user_streaks[user_id] = user_streaks.get(user_id, 0) + 1
    else:
        # Reset the streak if it's a new user
        user_streaks[user_id] = 1

    last_user = user_id  # Update the last user

    # Announce the streak
    streak_count = user_streaks[user_id]
    if streak_count > 5:  # Announce only if the streak is greater than 4
        # temporarily disable yap streaks
        print('yap')
        #await message.channel.send(f"{message.author.mention} is on a YAP streak with {streak_count} messages in a row!")
client.run(os.getenv('TOKEN'))
