from os import listdir
from os.path import isfile, join
import re

uuid_dir = "./uuids"

for filename in listdir(uuid_dir):
    filepath = join(uuid_dir, filename)

    if not isfile(filepath) or not filename.endswith(".txt"):
        continue

    print("Cleaning " + filename)

    text = ""

    with open(filepath, "r") as f:
        text = f.read() # Read the file

    text = re.sub("-", "", text) # Remove all hyphens
    text = re.sub("\n\n", "\n", text) # Remove unwanted new lines

    uuids = text.split("\n") # Turn into list
    uuids = list(set(uuids)) # Remove duplicates

    with open(filepath, "w") as f: # Save file
        f.write("\n".join(uuids))
