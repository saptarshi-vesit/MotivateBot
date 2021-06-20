import os
import discord
import requests
import json
import random
from replit import db
from keep_alive import keep_alive
client = discord.Client()

sad_words = ["sad", "depressed", "hurt", "remorseful", "angry", "gloomy", "miserable", "unhappy", "inferior", "inferiority", "incompetent", "worthless", "stupid", "idiot", "depressing", "sadness", "lamenting", "melancholy", "melancholic"]

encourage = [
  "Cheer Up!",
  "Everything is possible!",
  "Never give up!",
  "Relax!",
  "You are a great person",
  "You are beautiful!"
]

db["responding"] = True

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " - " + json_data[0]['a']
  return quote

def add_encourage(enc_message):
  if "encouragements" in db.keys():
    db["encouragements"].append(enc_message)
  else:
    db['encouragements'] = [enc_message]

def del_encourage(index):
  enc = db['encouragements']
  if len(enc) > index:
    del enc[index]
    db['encouragements'] = enc


@client.event
async def on_ready():
  print('Logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
  if message.author == client.user:
    return

  msg = message.content

  if msg.startswith('$inspire'):
    quote = get_quote()
    await message.channel.send(quote)
  
  if db["responding"]:
    more = encourage
    if "encouragements" in db.keys():
      more = more + list(db['encouragements'])

    if any(word in msg and not "$" in msg for word in sad_words):
      await message.channel.send(random.choice(more))

  if msg.startswith('$custom'):
    enc_message = msg.split("$custom ", 1)[1]
    add_encourage(enc_message)
    await message.channel.send("Successfully added")
  
  if msg.startswith('$del'):
    encouragements = []
    if "encouragements" in db.keys():
      index = int(msg.split("$del", 1)[1])
      del_encourage(index)
      encouragements = db['encouragements']
    await message.channel.send(encouragements) 
  
  if msg.startswith('$list'):
    encouragements = []
    if "encouragements" in db.keys():
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)
  
  if msg.startswith('$response'):
    value = msg.split("$response ", 1)[1]

    if value.lower() == "on":
      db['responding'] = True
      await message.channel.send("Response to words is on!")
    else:
      db['responding'] = False
      await message.channel.send("Response to words is off!")

keep_alive()
client.run(os.environ['TOKEN'])


