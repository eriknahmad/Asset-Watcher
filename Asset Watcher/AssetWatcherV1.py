# Project Name: Asset Watcher
# File Name: AssetWatcherV1.py
# Author: Erik Nahmad
# Date: March 24 2021
# Purpose: Proof of concept for an asset watcher.

import requests
import time

# A simple solution for watching crypto currency prices and notifying yourself if it exceeds specified thresholds. 

# 24/7 runtime using replit.com keep_alive - you can use Heroku or any other service.
# keep_alive()  

# For notifications you can use SMS, Telegram, Discord, etc.

coinList = [
  'BTC', 'ETH', 'ADA', 'XLM', 'CVC'
  ]

Thresholds = [
  BTC_L := 56000,
  BTC_H := 62000,
  ETH_L := 1900,
  ETH_H := 2100,
  ADA_L := 1.00,
  ADA_H := 1.30,
  XLM_L := 0.40,
  XLM_H := 0.50,
  CVC_L := 0.50,
  CVC_H := 0.90
  ]

Data_List = [
  responseList := [],
  requestJSON := [],
  coinNames := [],
  coinPrices := [],
  notifications := [],
  coinConditional := []
  ]

# Bot starts here
while True:
  
  # Clear lists each iteration
  i = 0
  while i < len(Data_List):
    Data_List[i].clear()
    i += 1
  i = 0
    
  endpoint = 'https://api.coinbase.com/v2/prices/{}-USD/spot'  # Source of price data
  while i < len(coinList):
    responseList.append(endpoint.format(coinList[i]))  # Request
    requestJSON.append(requests.get(responseList[i]).json())  # Store JSON Data
    coinNames.append(requestJSON[i]["data"]["base"])  # Parse Coin Name 
    coinPrices.append(requestJSON[i]["data"]["amount"])  # Parse Coin Price
    notifications.append(f"{coinNames[i]} Price: ${coinPrices[i][:8]}")  # Console / Push Notification
    time.sleep(0.3)
    print(notifications[i])

    # Conditional Statements for Notifications
    coinConditional.append(float(coinPrices[i]) < Thresholds[i * 2])  # If price is less than low threshold
    coinConditional.append(float(coinPrices[i]) > Thresholds[i * 2 + 1])  # If price is greater than high threshold
    
    ### DO NOTIFICATIONS WITH SMS, TELEGRAM, DISCORD, OR OTHER API. ###
    if coinConditional[i * 2]:
      pass  # This code runs if price is below threshold
    elif coinConditional[i * 2 + 1]:
      pass  # This code runs if price is above threshold

    i = i+1
  i = 0
  time.sleep(60)
  print("--------------------")
