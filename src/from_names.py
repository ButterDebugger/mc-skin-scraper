import random
from queue import Queue
from threading import Thread
import requests
import re
from os import makedirs
from os.path import exists

def generate_name(length):
    letters = "0123456789abcdefghijklmnopqrstuvwxyz_"
    name = ""

    for i in range(length):
        name += letters[random.randint(0, len(letters) - 1)]

    return name

def worker(backlog, length):
    used_names = []

    while True:
        name = generate_name(length)

        # Skip name if it's already been used
        if name in used_names:
            continue

        # Choose a random api to use
        match random.randint(0, 2):
            case 0:
                res = requests.get("https://api.ashcon.app/mojang/v2/user/" + name)

                if not res.status_code == 200:
                    used_names.append(name)
                    continue

                data = res.json()
                uuid = re.sub("-", "", data["uuid"])
                backlog.put((name, uuid))
            case 1:
                res = requests.get("https://playerdb.co/api/player/minecraft/" + name)

                if not res.status_code == 200:
                    used_names.append(name)
                    continue

                data = res.json()

                if not data["success"] == True:
                    used_names.append(name)
                    continue

                uuid = data["data"]["player"]["raw_id"]
                backlog.put((name, uuid))
            case 2:
                res = requests.get("https://api.minetools.eu/uuid/" + name)

                if not res.status_code == 200:
                    used_names.append(name)
                    continue

                data = res.json()

                if not data["status"] == "OK":
                    used_names.append(name)
                    continue

                uuid = data["id"]
                backlog.put((name, uuid))

def find_by_names():
    # Create folder and file if it doesn't exist
    if not exists("./uuids"):
        makedirs("./uuids")

    # Read old uuids
    if exists("./uuids/names.txt"):
        with open("./uuids/names.txt", "r") as f:
            uuids = f.read().split("\n")
    else:
        uuids = []

    # Start threads
    q = Queue()
    threads = 100

    for j in range(threads):
        thread = Thread(target=worker, args=(q, (j % 14) + 3))
        thread.daemon = True
        thread.start()

    # Take in uuids and append them to the data file
    try:
        with open("./uuids/names.txt", "a") as f:
            while True:
                name, uuid = q.get()

                if not uuid in uuids:
                    print("Found " + name + " -> " + uuid)
                    f.write(uuid + "\n")
    except KeyboardInterrupt:
        print("Process exited.")
        pass
