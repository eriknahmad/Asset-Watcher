# AssetWatcher
Cryptocurrency price watcher


# Motivation
I wrote this program to notify me if the price of an asset exceeds a specified thresholds. This chat bot is equipped with commands to dynamically update the watch list and thresholds. The bot runs 24/7 and uses a database to backup the data, in case of downtime.


# How to use?
Use Discord Developer Portal to create a bot, copy the API Key, and use [Replit](https://www.replit.com) IDE to:
- Insert Discord API Key into script.
- Copy your servers unique ID, server owners ID, and a spam channel ID.
- Replace Server, Owner, and Spam_Channel Variables with each ID.
- Run the script and use /help for commands.

For now you need to use Replit until I integrate a database like MongoDB. Use Replit's Keep Alive Script and copy the flask website url it generates. Use [UptimeRobot](https://www.uptimerobot.com) or something similar to ping the flask website to keep it up 24/7.


# Contribute
Contributions, issues and feature requests are welcome.


# Author
Erik Nahmad
- Discord: Myth#0548
- Email: eriknahmad@gmail.com


# License
Copyright © 2022 [Erik Nahmad](https://github.com/eriknahmad).<br />
This project is [MIT](https://github.com/eriknahmad/Asset-Watcher/blob/main/LICENSE) licensed.
