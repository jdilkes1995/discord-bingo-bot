import discord
import os
import asyncio
from discord.ext import commands
from dotenv import load_dotenv



load_dotenv()
token = os.getenv('KEY')

client = commands.Bot(command_prefix='!', intents=discord.Intents.all())

async def load():
    for filename in os.listdir('bot/cogs'):
        if filename.endswith('.py'):
            await client.load_extension(f'cogs.{filename[:-3]}')

async def main():
    await load()
    await client.start(token)

asyncio.run(main())


