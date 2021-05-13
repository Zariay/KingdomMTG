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
kingdomGame = {}

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

@client.event
async def on_guild_join(guild):
  await guild.send("Thanks for adding me! Use !info for more info, and be sure to restrict me to the proper channel!")

@bot.command(name = 'join')
async def _join(ctx):
  if(len(players) == 0):
    players.append(ctx.author)
    await ctx.send("Starting a lobby.")
  else: 
    if ctx.author not in players:
      await ctx.send("Welcome to the game!")
      players.append(ctx.author)
      return
    else:
      await ctx.send("You've already joined. No need to rejoin again, just wait for more players.")
      return
  if len(players) == 6:
    kingRoles.append("Usurper")
  
  
@bot.command(name = 'start')
async def _start(ctx):
  global gameStart
  if not gameStart:
    if len(players) < 5:
      await ctx.send("Cannot start the game! Not enough players. There are (is) only " + str(len(players)) + " player(s) in the lobby so far.")
      return
    elif len(players) > 6: 
      await ctx.send("There are " + str(len(players)) + " players in the lobby. Cannot start game.")
      return
    else:
      random.shuffle(kingRoles)
      random.shuffle(players)
      gameStart = not gameStart
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
  await ctx.send("Use the !turnorder command to see what they turn order is in case you forget.")
  await ctx.send("Use the !leave command to drop from the lobby.")
  await ctx.send("Use the !cleargame command to reset the lobby.")
  await ctx.send("Use the !roles command to remind yourself what each role is!")

@bot.command(name = 'leave')
async def _leave(ctx):
  if ctx.author in players:
    players.remove(ctx.author)
  else:
    await ctx.send("You've already left.")

@bot.command(name = 'roles')
async def _roles(ctx):
  await ctx.send("King: Starts with 50 life. Teams up with the Knight to defeat everyone else.")
  await ctx.send("Knight: Teams with the King and does his best to protect him. Wins if the King wins as well, but also loses if the King loses.")
  await ctx.send("Bandits: Only goal is to just kill the king.")
  await ctx.send("Assassin: They must kill everyone else before the king.")
  await ctx.send("Usurper: If they kill the King, they reset back to 50 life and become the new King.")

@bot.command(name = 'checklobby')
async def _checklobby(ctx):
  for gamers in gameArray:
    await ctx.send(gamers.name)
      
@bot.command(name = 'cleargame')
async def _cleargame(ctx):
  global gameStart
  if(len(gameArray) == 0 and len(players) == 0):
    await ctx.send("Lobby is empty")
  else:
    gameArray.clear()
    players.clear()
    if(len(kingRoles) == 6):
      kingRoles.remove("Usurper")
    await ctx.send("Cleared the lobby")
    if not gameStart:
      gameStart = not gameStart

def setTurnOrder():
  for i in range(0, len(gameArray)):
    if(gameArray[i][1] == "King"):
      gameArray.insert(0, gameArray.pop(i))
  shuffleRestArray = gameArray[0:]
  random.shuffle(shuffleRestArray)
  gameArray[0:] = shuffleRestArray

keep_alive()
bot.run(token)
