# Minecraft Skin Scraper

A simple project created in Python with the goal of obtaining an unlimited supply of Minecraft skins.

## Methods

*`clean_uuids.py`*
Used to filter out duplicates and reformats all uuid lists

*`find_uuids.py`*
Used to generate uuids using two methods:
1. *`from_names.py`* Randomly generated usernames to uuids
2. *`namemc_hearts.py`* Grab uuids from players who heart minecraft servers on NameMC

*`get_skins.py`*
Scans through every uuid lists and converts uuids to skins

*`listing.py`*
Used to get skins published onto Minecraft skin gallery websites

## Lists

All lists containing uuids should be stored in the `uuids` directory. Pre-made lists are available to download with the links provided below:

1. *`q.txt`* Large list of hypixel player uuids from [this thread](https://hypixel.net/threads/mc-player-uuid-list-7-000-000.4706530/)
2. *`kaggle.txt`* Large list of minecraft uuids taken from [this database](https://www.kaggle.com/datasets/sha2048/minecraft-skin-dataset?select=Skins)
