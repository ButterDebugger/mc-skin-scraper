import requests
from os.path import exists
import time
import re

servers = [
    # "purple.wtf",
    # "cavepvp.org",
    # "play.vipermc.net",
    # "pvp.land",
    # "mc.hypixel.net",
    # "akumamc.net",
    # "play.wildprison.net",
    # "bridger.land",
    # "oplegends.com",
    # "sagepvp.org",
    # "dynamicpvp.net",
    # "mcplayhd.net",
    # "astralmc.cc",
    # "coldpvp.com",
    # "lunar.gg",
    # "minemen.club",
    # "bwhub.net",
    "onlypvp.pl",
    "ghostly.live",
    "greev.eu",
    "sololegends.net",
    "play.schoolrp.net",
    "holypvp.net",
    "hazelmc.com",
    "mc.mantle.gg",
    "play.wynncraft.com",
    "bedwarspractice.club",
    "ilovecatgirls.xyz",
    "2b2t.org",
    "skyblock.net",
    "play.ecc.eco",
    "play.cubecraft.net",
    "invadedlands.net",
    "us.mineplex.com",
    "funcraft.net",
    "redesky.com"
]

def grab_likers():
    with open("./uuids/names.txt", "r") as f:
        old_uuids = f.read().split("\n")

    for server in servers:
        print(server)

        while True:
            time.sleep(0.5)

            res = requests.get("https://api.namemc.com/server/" + server + "/likes")

            if not res.status_code == 200:
                print("Rate limited... Retrying in 60 seconds :(")
                time.sleep(60)
                continue

            likes = res.json()
            break

        # Save new uuids
        with open("namemclikers.txt", "a") as f:
            for uuid in likes:
                if uuid not in old_uuids:
                    f.write("\n" + re.sub("-", "", uuid))

