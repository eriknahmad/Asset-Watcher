# Project Name: Asset Watcher
# File Name: AssetWatcherV1.py
# Author: Erik Nahmad
# Date: August 05 2021
# Purpose: Scrape and compare cryptocurrency prices to user defined thresholds

import discord
import requests
from replit import db
from discord.ext import commands, tasks
from KeepAlive import keep_alive

TOKEN = "APIKEY"  # API Key
Server = 0  # Put Server ID here
Owner = 0  # Put Server Owner ID here
Spam_Channel = 0  # Put Spam Channel ID here

client = discord.Client()  # Init Discord Client
bot = commands.Bot(command_prefix=["/", "!", "?", "$"])  # Command Prefixes
Request = "https://api.coinbase.com/v2/prices/{}-USD/spot"  # Request price data

CoinList = []  # Lists pulled from Database
PriceList = []
Thresholds = []

Data_List = [  # Lists storing asset data
  Req_List  := [],
  JSON_List := [],
  C_NAMES := [],
  C_PRICES := [],
  Push_List := []
]

# 24/7 uptime
keep_alive()


@bot.event
async def on_ready():
  global member
  print(f'We have logged in as {bot.user.name}')
  server = bot.get_guild(Server)
  member = await server.fetch_member(Owner)
  await member.send("Bot Is Online!")
  DatabasePull()  # Populate lists from Database if possible



# Clear messages in the current channel. Optional Parameter: amount
@bot.command(name="clear", brief="Clear Chat", aliases=["c"])
async def clear(cmd, amount=20):
  await cmd.channel.purge(limit=amount)



# Watch an asset by currency code (eg. BTC). 
# For Threshold Parameter set a number as a percentage bounds above and below. 
# (example: if coinprice = 100 and threshold = 50% then low_bounds = 50 and high_bounds = 150).
# Alert user if the price of the asset reaches 50 or 150.
@bot.command(name="watch", brief="Watch An Asset", aliases=["w"])
async def watch(cmd, Coin=None, Threshold=10):
  Status = requests.get(Request.format(Coin)).status_code  # Response Code
  if Coin != None and Status != 404:  # if valid code is sent
    CoinList.append(Coin.upper())  # append coin to list
    Thresholds.append(Threshold)  # append threshold to list
    i = -1  # Index position for last element
    CoinData(i)  # Update data for newly added coin
    PriceList.append(C_PRICES[i])  # Coin price
    DatabaseStore()  # Store Coin Name, Price, and Threshold
    CurrentPrice = f"```{Push_List[i]}\n"
    Threshold = f"Threshold: {Thresholds[i]}%```"
    Price_List = CurrentPrice + Threshold
    await cmd.send(Price_List)
  elif Coin == None or Status == 404:  # No Coin or Invalid Coin
    await cmd.send("That asset is not in my database.")



# Display Watchlist: Coin Name, Coin Price, Watch Point, and Threshold.
@bot.command(name="price", brief="Display Watchlist", aliases=["p", "pl"])
async def price(cmd, Index=None):

  if Index is None:
    y = 0
    DataClear()
    while y < len(CoinList):  # Display Watchlist
      CoinData(y)
      CurrentPrice = f"```{Push_List[y]}\n"
      CoinPrice = float(PriceList[y])
      Threshold = int(Thresholds[y])
      WP = CoinPrice + (CoinPrice / 100 * Threshold)
      WatchPoint = f"Watch Point: ${WP}\n"
      Threshold = f"Threshold: {Thresholds[y]}%```"
      Price_List = CurrentPrice + WatchPoint + Threshold
      await cmd.channel.send(Price_List)
      y += 1

  elif int(Index) >= len(CoinList):  # Index out of bounds
    await cmd.channel.send(f"```No Value at Index {Index}```")
    
  elif int(Index) < len(CoinList):  # Price of Coin by Index
    i = int(Index)
    CurrentPrice = f"```{Push_List[i]}\n"
    CoinPrice = float(PriceList[i])
    Threshold = int(Thresholds[i])
    WP = CoinPrice + (CoinPrice / 100 * Threshold)
    WatchPoint = f"Watch Point: ${WP}\n"
    Threshold = f"Threshold: {Thresholds[i]}%```"
    PriceByIndex = CurrentPrice + WatchPoint + Threshold
    await cmd.channel.send(PriceByIndex)



# Delete a Coin by Index or Change a Threshold by Index
@bot.command(name="delete", brief="Delete Coin", aliases=["d", "dc"])
async def delete(cmd, Index=None, Threshold=None):
  i = int(Index)
  
  if Threshold == None and i < len(CoinList):  # if valid index is sent
    await cmd.channel.send(f"```Deleting {CoinList[i]}```")  # Delete message
    DatabaseDel(i)  # Remove item by Index then update database
    ReloadData()   # Reload data
    DatabaseStore()  # Store New Data

  elif Threshold != None and i < len(CoinList):  # Change Threshold
    Thresholds[i] = int(Threshold)  # Set the list value equal to parameter
    NewThreshold = f"```{CoinList[i]} Threshold: {Thresholds[i]}%```"
    await cmd.channel.send(NewThreshold)  # Display new threshold
    DatabaseStore()  # Store New Data

  else:
    await cmd.channel.send(f"```No Value at Index {Index}```")
    


# Background Task collecting data every minute.
@tasks.loop(seconds=60)
async def price():
  spam_channel = bot.get_channel(Spam_Channel)  # Spam Channel
  server = bot.get_guild(Server)  # Server
  member = await server.fetch_member(Owner)  # Owner
  DataClear()  # Clear Lists
  i = 0
  while i < len(CoinList):
    CoinData(i)  # Refresh Price Data
    CoinName = str(C_NAMES[i])
    CoinPrice = float(PriceList[i])
    Threshold = int(Thresholds[i])

    High_Threshold = CoinPrice + (CoinPrice / 100 * Threshold)
    Low_Threshold = CoinPrice - (CoinPrice / 100 * Threshold)
    print(Push_List[i][:20])

    # Conditional Boolean for Notifications
    Alert = f"{CoinName} is"
    Up = f"{Alert} up {Threshold}%"
    Down = f"{Alert} down {Threshold}%"
    if CoinPrice >= High_Threshold:
      await member.send(f"```{Up}```")
      print("high")
    elif CoinPrice <= Low_Threshold:
      await member.send(f"```{Down}```")
      print("low")

    i += 1
  i = 0
  spam = '\n'.join(Push_List)
  await spam_channel.send(f'```{spam}```')
  print("-----------------")



def DataClear():  # Clear list data
  for x in Data_List:
    x.clear()



def CoinData(i):  # Update coin data
  Req_List.append(Request.format(CoinList[i]))
  JSON_List.append(requests.get(Req_List[i]).json())
  C_NAMES.append(JSON_List[i]['data']['base'])
  C_PRICES.append(str(JSON_List[i]['data']['amount']))
  Push_List.append(f"{C_NAMES[i]} Price: ${C_PRICES[i][:8]}")



def ReloadData():  # Reload all list data
  DataClear()
  i = 0
  while i < len(CoinList):
    CoinData(i)
    i += 1



def DatabaseStore():  # Store list elements in Database
  db["CoinList"] = CoinList
  db["PriceList"] = PriceList
  db["Thresholds"] = Thresholds



def DatabasePull():  # Copy Database to lists
  try:
    for x in db["CoinList"]:
      CoinList.append(x)
    for x in db["PriceList"]:
      PriceList.append(x)
    for x in db["Thresholds"]:
      Thresholds.append(x)
    price.start()
  except KeyError:
    print("Database is empty")



def DatabaseDel(i):  # Delete list element
  CoinList.pop(i)
  PriceList.pop(i)
  Thresholds.pop(i)
  DatabaseStore()



bot.run(TOKEN)
