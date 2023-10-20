import time
import requests
from os.path import exists
import threading
import random

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"}
threads = 100
uuids = open("uuids.txt", "r").read().split("\n")

# Define worker method
def worker(chunk, chunks):
	apicycle = random.randint(0, 3)

	for i in range(chunk, len(uuids), chunks):
		uuid = uuids[i]
		filename = "skins/" + uuid

		# Skip existing
		if exists(filename + ".png"):
			continue
		elif exists(filename + ".unknown"):
			continue
		
		# Cycle through APIs to less strain them
		if apicycle == 0:
			res = requests.get("https://crafatar.com/skins/" + uuid)
		elif apicycle == 1:
			res = requests.get("https://minotar.net/skin/" + uuid)
		elif apicycle == 2:
			res = requests.get("https://mineskin.eu/skin/" + uuid)
		elif apicycle == 3:
			res = requests.get("https://api.mineatar.io/skin/" + uuid)
		
		# Increment API cycle
		apicycle += 1

		if apicycle > 3:
			apicycle = 0

		# Check if response is valid
		if not res.status_code == 200:
			with open(filename + ".unknown", "w") as f:
				f.write("")
			continue

		print(uuid) # Print uuid

		with open(filename + ".png", "wb") as f: # Write the file
			f.write(res.content)

# Start threads
for j in range(threads):
	thread = threading.Thread(target=worker, args=[j, threads])
	thread.daemon = True
	thread.start()

# Keep main process alive
try:
	while True:
		time.sleep(1)
except KeyboardInterrupt:
	print("Process exited.")
	pass