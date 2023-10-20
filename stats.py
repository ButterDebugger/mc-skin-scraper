from os import listdir

totalskins = 0

# Display stats for the lists
uuids = 0
q = 0
kaggle = 0
namemclikers = 0
names = 0

with open("uuids.txt", "r") as f:
	for line in f:
		uuids += 1

with open("q.txt", "r") as f:
	for line in f:
		q += 1

with open("kaggle.txt", "r") as f:
	for line in f:
		kaggle += 1

with open("namemclikers.txt", "r") as f:
	for line in f:
		namemclikers += 1

with open("names.txt", "r") as f:
	for line in f:
		names += 1

print("List stats:")
print("  uuids.txt:", uuids)
print("  q.txt:", q)
print("  kaggle.txt:", kaggle)
print("  namemclikers.txt:", namemclikers)
print("  names.txt:", names)

# Display stats for novaskins
skins = 0
unavailable = 0

for file in listdir("novaskin/"):
	if file.endswith(".png"):
		skins += 1
	elif file.endswith(".unavailable"):
		unavailable += 1

print("Novaskin stats:")
print("  Skins:", skins)
print("  Unavailable:", unavailable)
print("  Indexed:", skins + unavailable)

totalskins += skins # Add to total

# Display stats for skindex
skins = 0
unavailable = 0

for file in listdir("skindex/"):
	if file.endswith(".png"):
		skins += 1
	elif file.endswith(".unavailable"):
		unavailable += 1

print("Skindex stats:")
print("  Skins:", skins)
print("  Unavailable:", unavailable)
print("  Indexed:", skins + unavailable)

totalskins += skins # Add to total

# Display stats for uuid skins
skins = 0
unknown = 0

for file in listdir("skins/"):
	if file.endswith(".png"):
		skins += 1
	elif file.endswith(".unknown"):
		unknown += 1

print("Skins stats:")
print("  Skins:", skins)
print("  Unknown:", unknown)
print("  Completion:", str((skins + unknown) / uuids * 100) + "%")

totalskins += skins # Add to total

# Display stats for total skins
print("Total skins:", totalskins)