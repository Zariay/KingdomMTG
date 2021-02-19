import discord
import os
import random

from discord.ext import commands
from keep_alive import keep_alive
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('TOKEN')
client = discord.Client()

bot = commands.Bot(command_prefix = '!')

kingRoles = ["King", "Knight", "Bandit", "Bandit", "Assassin"]
players = []
gameArray = []
gameStart = False

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

@client.event
async def on_guild_join(guild):
  await guild.send("Thanks for adding me! Use !info for more info, and be sure to restrict me to the proper channel!")

@bot.command(name = 'join')
async def _join(ctx):
  players.append(ctx.author)
  for player in players:
    if player != ctx.author:
      await ctx.send("Welcome to the game!")
      return
    else:
      await ctx.send("You've already joined. No need to rejoin again, just wait for more players.")
      players.remove(ctx.author)
  if len(players) == 6:
    kingRoles.append("Ursurper")
  
  
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
      for i in range(0, len(players)):
        if(kingRoles[i] == "King"):
          await ctx.send(players[i].mention + " is the king!")
        else:
          await players[i].send("Your role is the " + kingRoles[i])
        gameArray.append([players[i], kingRoles[i]])
      setTurnOrder()
  else:
    await ctx.send("Game in progress");

@bot.command(name = 'turnorder')
async def _turnorder(ctx):
  for i in range(0, len(gameArray)):
    await ctx.send(str(i + 1) + ". " + gameArray[i][0].name)

@bot.command(name = 'info')
async def _info(ctx):
  await ctx.send("Welcome to the Kingdom MTG bot! This bot is meant to make assigning kingdom roles much simpler for you.")
  await ctx.send("Use the !join command to join the lobby for the game.")
  await ctx.send("Use the !start command to assign everyone's roles.")
  await ctx.send("Use the !turnorder command to see what the current turn order is in case you forget.")
  await ctx.send("Use the !leave command to drop from the lobby.")
  await ctx.send("Use the !cleargame command to reset the lobby.")
  await ctx.send("Use the !roles command to remind yourself what each role is!")

@bot.command(name = 'leave')
async def _leave(ctx):
  for player in players:
    if player == ctx.author:
      players.remove(ctx.author)
    else:
      await ctx.send("You've already left.")
      
@bot.command(name = 'cleargame')
async def _cleargame(ctx):
  if(len(gameArray) == 0 and len(players) == 0):
    await ctx.send("Lobby is empty")
  else:
    gameArray.clear()
    players.clear()
    if(len(kingRoles) == 6):
      kingRoles.remove("Ursurper")
    await ctx.send("Cleared the lobby")
    if gameStart:
      not gameStart

def setTurnOrder():
  for i in range(0, len(gameArray)):
    if(gameArray[i][1] == "King"):
      gameArray.insert(0, gameArray.pop(i))
  shuffleRestArray = gameArray[0:]
  random.shuffle(shuffleRestArray)
  gameArray[0:] = shuffleRestArray

keep_alive()
bot.run(token)
