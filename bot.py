import discord
from dotenv import load_dotenv
import os
import requests as req
import json
import wikipedia
from datetime import datetime

load_dotenv()

def get_meme():
    response = req.get("https://meme-api.com/gimme")
    json_data = json.loads(response.text)
    return json_data['url']

def get_date_today():
    now = datetime.now()
    date_today = now.strftime(f"%d/%m/%Y %H:%M:%S") 
    return date_today

def get_wiki(search):
    max_lenght = 2000
    wikipedia.set_lang("id")
    try:
        summary = wikipedia.summary(search, sentences=3)
        if len(summary) > max_lenght:
            return summary[:max_lenght] + "..."
        return summary
    except wikipedia.DisambiguationError as e:
        return f"Your search term '{search}' may refer to multiple topics. Please be more specific. Options include: {e.options[:5]}"
    except wikipedia.PageError:
        return f"No page found for '{search}'. Please check your spelling or try a different term."
    return wikipedia.summary(search)

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}')
    
    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        if message.content.startswith('$hello'):
            await message.channel.send('Hello WOrld!')
        
        if message.content.startswith('$meme'):
            await message.channel.send(get_meme())
        
        if message.content.startswith('$wiki'):
            search = message.content[6:]
            await message.channel.send(get_wiki(search))
        
        if message.content.startswith('$date'):
            await message.channel.send(get_date_today())
        

token = os.getenv("API_TOKEN")

intents = discord.Intents.default()
intents.message_content = True  # Enable the message content intent

Client = MyClient(intents=intents)
Client.run(token)