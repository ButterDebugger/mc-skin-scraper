import requests
from os.path import exists
import time
import re

servers = [
	"purple.wtf",
	"cavepvp.org",
	"play.vipermc.net",
	"pvp.land",
	"mc.hypixel.net",
	"akumamc.net",
	"play.wildprison.net",
	"bridger.land",
	"oplegends.com",
	"sagepvp.org",
	"dynamicpvp.net",
	"mcplayhd.net",
	"astralmc.cc",
	"coldpvp.com",
	"lunar.gg",
	"minemen.club",
	"bwhub.net",
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

uuids = []

for server in servers:
	print(server)
	while True:
		time.sleep(10)

		res = requests.get("https://api.namemc.com/server/" + server + "/likes")
		if not res.status_code == 200:
			print("ratelimited...")
			time.sleep(10)
			continue
		
		likes = res.json()
		break
	
	uuids.extend(likes)

with open("namemclikers.txt", "w") as f: # Save file
	text = "\n".join(uuids)
	text = re.sub("-", "", text)
	f.write(text)
