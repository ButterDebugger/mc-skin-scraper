import requests
from os.path import exists
import threading
import time

# Note: The NovaSkin scraper have been disabled due to NovaSkin's content not always being... skins.

threads = 20 # Number of threads per searchee (x2)

def worker(searchee, start, chunks):
	if searchee == "skindex":
		folderpath = "./skindex/"
		baseurl = "https://www.minecraftskins.com/skin/download/{id}"
	# elif searchee == "novaskin":
	# 	folderpath = "./novaskin/"
	# 	baseurl = "https://minecraft.novaskin.me/skin/{id}/download"
	else:
		print("Invalid choice.")
		return

	skinid = start
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36'}

	while True:
		filename = folderpath + str(skinid)
		url = baseurl.replace("{id}", str(skinid))
		
		# Skip existing
		if exists(filename + ".png"):
			skinid += chunks # Increment skin id
			continue
		elif exists(filename + ".unavailable"):
			skinid += chunks # Increment skin id
			continue
		
		# Make download request
		res = requests.get(url, headers=headers)
		
		# Skip unavailable
		if not res.status_code == 200:
			open(filename + ".unavailable", "w").write("")
			skinid += chunks # Increment skin id
			continue
		
		print(searchee + " \t" + str(skinid)) # Print current skin id
		
		open(filename + ".png", "wb").write(res.content) # Write image

		skinid += chunks # Increment skin id

# Start threads
print("Searching skindex...")
for j in range(threads):
	thread = threading.Thread(target=worker, args=["skindex", j, threads])
	thread.daemon = True
	thread.start()

# print("Searching novaskin...")
# for j in range(threads):
# 	thread = threading.Thread(target=worker, args=["novaskin", j, threads])
# 	thread.daemon = True
# 	thread.start()

# Keep main process alive
try:
	while True:
		time.sleep(1)
except KeyboardInterrupt:
	print("Process exited.")
	pass