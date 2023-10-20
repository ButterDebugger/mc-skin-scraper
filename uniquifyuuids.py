import re

text = ""

with open("uuids.txt", "r") as f:
	text = f.read() # Read the file

text = re.sub("-", "", text) # Remove all hyphens
text = re.sub("\n\n", "\n", text) # Remove unwanted new lines

uuids = text.split("\n") # Turn into list
uuids = list(dict.fromkeys(uuids)) # Remove duplicates

with open("uuids.txt", "w") as f: # Save file
	f.write("\n".join(uuids))
