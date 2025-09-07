import json
from os import listdir
from os.path import isfile, join, exists

uuid_dir = "./uuids"

# Read list depth data
depth_path = join(uuid_dir, "depth.json")

if not exists(depth_path):
    with open(depth_path, "w") as f:
        f.write("{}")

f = open(depth_path, "r")
depth_data = json.loads(f.read())
f.close()

# Declare saving function
def save_depth():
    try:
        with open(depth_path, "w") as f:
            f.write(json.dumps(depth_data, indent = 4))
    except KeyboardInterrupt:
        print("Cancelled keyboard interrupt due to saving depth data")

# Read uuid files
filenames = []

for filename in listdir(uuid_dir):
    filepath = join(uuid_dir, filename)

    if not isfile(filepath) or not filename.endswith(".txt"):
        continue

    if filename not in depth_data:
        depth_data[filename] = 0

    filenames.append(filename)

save_depth()

def read_uuids():
    for filename in filenames:
        filepath = join(uuid_dir, filename)

        with open(filepath, "r") as f:
            uuids = f.read().split("\n")

            for i in range(len(uuids)):
                if i < depth_data[filename]:
                    continue

                depth_data[filename] += 1

                yield uuids[i]
