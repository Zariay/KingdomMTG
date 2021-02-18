import discord
import os
import random

from discord.ext import commands
from discord.ext.commands import Bot

from dotenv import load_dotenv

load_dotenv()
token = os.getenv('TOKEN')
client = discord.Client()

bot = commands.Bot(command_prefix = '!')

kingRoles = ["King", "Knight", "Bandit", "Bandit", "Assassin"]
players = []
gameStart = False

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

@bot.command(name = 'join')
async def _join(ctx):
  players.append(ctx.author)
  #for player in players:
    #await ctx.send(player.username)
  if len(players) == 6:
    kingRoles.append("Ursurper")
  for player in players:
    if player == ctx.author:
      await ctx.send("You've already joined. No need to rejoin again, just wait for more players.")
    else:
      await ctx.send("Welcome to the game!")
  
@bot.command(name = 'start')
async def _start(ctx):
  if not gameStart:
    if len(players) < 5:
      await ctx.send("Cannot start the game! Not enough roles.")
      return
    elif len(players) > 6: 
      await ctx.send("Too many players! Can't start.")
      return
    else:
      random.shuffle(kingRoles)
      random.shuffle(players)
      not gameStart
      count = 0
      for player in players:
        await player.send("Your role is the " + kingRoles[count])
        if(kingRoles[count] == "King"):
          await ctx.send(players[count].name + " is the king!")
        count += 1
  else:
    await ctx.send("Game in progress");

#@bot.command(name = 'turnorder')
#async def _turnorder(ctx):


@bot.command(name = 'leave')
async def _leave(ctx):
  for player in players:
    if player == ctx.author:
      players.remove(ctx.author)
    else:
      await ctx.send("You've already left.")
      
@bot.command(name = 'cleargame')
async def _cleargame(ctx):
  players.clear()
  kingRoles.remove("Ursurper")
  await ctx.send("Cleared the lobby")
  if gameStart:
    not gameStart

bot.run(token)
