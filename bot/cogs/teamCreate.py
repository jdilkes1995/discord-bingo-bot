import aiosqlite
import discord
import aiosqlite
from discord.ext import commands
import traceback

DB_PATH = 'teams.db'

class Create(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Bot is running")
        print("Database setup complete")
    

    #Command that registers teams

    @commands.command()
    async def createTeam(self, ctx: commands.Context, teamName: str):
        try:
            async with aiosqlite.connect(DB_PATH) as db:
                await db.execute('INSERT INTO users (teamName) VALUES (?)', (teamName))
                await db.commit()
            await ctx.send(f"You have successfully created the team {teamName}")
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
                    text+=f"Team ID: {_id} - Team Name: {name}\n"
            await ctx.send(f"{text}")
            
    @commands.command()
    async def dom(self, ctx: commands.Context):
        await ctx.send('Your mums a sweaty doggy whore')

async def setup(bot):
    await bot.add_cog(Create(bot))