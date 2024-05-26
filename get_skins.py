import requests
from os import makedirs
from os.path import exists, join
from uuid_reader import read_uuids, save_depth
from queue import Queue
import hashlib
import random
from threading import Thread

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"}

def worker(queue):
    while True:
        uuid = queue.get()

        # Choose a random api to use
        match random.randint(0, 3):
            case 0:
                res = requests.get("https://crafatar.com/skins/" + uuid)
            case 1:
                res = requests.get("https://minotar.net/skin/" + uuid)
            case 2:
                res = requests.get("https://mineskin.eu/skin/" + uuid)
            case 3:
                res = requests.get("https://api.mineatar.io/skin/" + uuid)

        # Check if response is valid
        if not res.status_code == 200:
            queue.task_done()
            continue

        content = res.content

        # Check if file is a valid png
        if not content.startswith(b"\x89\x50\x4E\x47\x0D\x0A\x1A\x0A"):
            queue.task_done()
            continue

        # Save the skin
        hash = hashlib.sha256(res.content).hexdigest()
        filepath = join("./skins", hash[:2], hash + ".png")

        with open(filepath, "wb") as f:
            f.write(content)

        queue.task_done()

# Create directory tree
for x in [*"0123456789abcdef"]:
    for y in [*"0123456789abcdef"]:
        dir_path = join("./skins", x + y)

        if not exists(dir_path):
            makedirs(dir_path)

# Start worker threads
uuid_queue = Queue(maxsize=0)
num_threads = 20

for i in range(num_threads):
    thread = Thread(target=worker, args=(uuid_queue,))
    thread.daemon = True
    thread.start()

# Start reading uuids
has_more = True
batch_size = num_threads
uuid_gen = read_uuids()

while has_more:
    try:
        for x in range(batch_size):
            uuid_queue.put(next(uuid_gen))
    except StopIteration:
        has_more = False

    uuid_queue.join()
    save_depth()

    print("Batch done")
