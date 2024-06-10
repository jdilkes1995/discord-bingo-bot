import aiosqlite
import discord
import aiosqlite
from discord.ext import commands
import traceback

import discord.ext
import discord.ext.commands

DB_PATH = 'teams.db'

class Create(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    teamName TEXT,
                    member TEXT
                )
            ''')
            await db.commit()
    print("Database setup complete")
    print("Bot is running")

    

    #Command that registers teams

    @commands.command()
    async def createTeam(self, ctx: commands.Context, teamName: str, members: commands.Greedy[discord.Member]):
        try:
            async with aiosqlite.connect(DB_PATH) as db:
                id = ", ".join([str(member.id) for member in members])
                print(id)
                await db.execute('INSERT INTO users (teamName, member) VALUES (?, ?)', (teamName, id))
                await db.commit()
            await ctx.send(f"You have successfully created the team {teamName} with Members: {id}")
        except Exception as e:
            print(f"Error creating team: {e}")
            traceback.print_exc()
            await ctx.send(f"Failed to create team {teamName}. Please try again.")


    #Command that gets all teams

    @commands.command()
    async def getTeam(self, ctx: commands.Context):
            async with aiosqlite.connect(DB_PATH) as db:
                cur = await db.execute("SELECT * FROM users")
                data = await cur.fetchall()
                text = ""
                for team in data:
                    _id = team[0]
                    name = team[1]
                    member = team[2]
                    members_string = member.split(', ')
                    memberMention = [f"<@{_id}>" for _id in members_string]
                    memberJoin = ", ".join(memberMention)
                    text+=f"Team ID: {_id} - Team Name: {name} - Team Members: {memberJoin}\n"
            await ctx.send(f"{text}")

    @commands.command()
    async def test(self, ctx: commands.Context, members: commands.Greedy[discord.Member], dogs = None):
        id = ", ".join([str(member.id) for member in members])
        print(dogs)
        print(id)
        await ctx.send(f"{id}")

async def setup(bot):
    await bot.add_cog(Create(bot))
