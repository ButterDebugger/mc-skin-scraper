import random
import threading
import requests
import re
import time

letters = "0123456789abcdefghijklmnopqrstuvwxyz_"
threads = 100
notnames = []
uuids = open("names.txt", "r").read().split("\n")

def createName():
	name = ""
	for _ in range(random.randint(3, 16)):
		name += letters[random.randint(0, len(letters) - 1)]
	return name

def worker():
	while True:
		name = createName()
		uuid = None

		# Skip name if it's already been used
		if name in notnames:
			continue

		# Choose a random api to use
		match random.randint(0, 2):
			case 0:
				res = requests.get("https://api.ashcon.app/mojang/v1/user/" + name)

				if not res.status_code == 200:
					notnames.append(name)
					continue

				data = res.json()
				uuid = re.sub("-", "", data["uuid"])
			case 1:
				res = requests.get("https://playerdb.co/api/player/minecraft/" + name)

				if not res.status_code == 200:
					notnames.append(name)
					continue

				data = res.json()

				if not data["success"] == True:
					notnames.append(name)
					continue
				
				uuid = data["data"]["player"]["raw_id"]
			case 2:
				res = requests.get("https://api.minetools.eu/uuid/" + name)

				if not res.status_code == 200:
					notnames.append(name)
					continue

				data = res.json()

				if not data["status"] == "OK":
					notnames.append(name)
					continue

				uuid = data["id"]

		print(uuid, name) # Print the uuid

		if uuid not in uuids: # Check if uuid is not already in list
			uuids.append(uuid) # Add uuid to list
		
		notnames.append(name) # Add name to list

# Start threads
for j in range(threads):
	thread = threading.Thread(target=worker)
	thread.daemon = True
	thread.start()

# Keep main process alive
try:
	while True:
		time.sleep(15)
		print("Saving...")
		with open("names.txt", "w") as f:
			f.write("\n".join(uuids))
except KeyboardInterrupt:
	print("Process exited.")
	pass
