import requests
from os.path import exists
import threading
import time
import os

download_entries = {
    "skindex": "https://www.minecraftskins.com/skin/download/{id}",
    "novaskin": "https://minecraft.novaskin.me/skin/{id}/download"
}

def worker(entry, start, chunks):
    folder_path = f"./{entry}/"
    base_url = download_entries[entry]

    skin_id = start
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36'}

    while True:
        filename = folder_path + str(skin_id)
        url = base_url.replace("{id}", str(skin_id))

        # Skip existing
        if exists(filename + ".png"):
            skin_id += chunks # Increment skin id
            continue
        elif exists(filename + ".unavailable"):
            skin_id += chunks # Increment skin id
            continue

        # Make download request
        res = requests.get(url, headers=headers)

        # Skip unavailable
        if not res.status_code == 200:
            open(filename + ".unavailable", "w").write("")
            skin_id += chunks # Increment skin id
            continue

        print(entry + " \t" + str(skin_id)) # Print current skin id

        open(filename + ".png", "wb").write(res.content) # Write image

        skin_id += chunks # Increment skin id

def start_search(entry, threads = 20):
    print(f"Searching {entry}...")

    # Create folder if it doesn't exist
    if not exists(f"./{entry}/"):
        os.makedirs(f"./{entry}/")

    # Start threads
    for j in range(threads):
        thread = threading.Thread(target=worker, args=[entry, j, threads])
        thread.daemon = True
        thread.start()

    # Keep main process alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Process exited.")
        pass

if __name__ == "__main__":
    threads = 20

    while True:
        threads = input("Enter number of threads: ")
        if threads == "":
            threads = 20

            print("Using default value of 20.")
            break
        elif threads.isdigit():
            threads = int(threads)
            break
        else:
            print("Invalid number.")

    while True:
        match input("Search for [S]kindex or [N]ovaskin? ").upper():
            case "S":
                start_search("skindex")
                break
            case "N":
                start_search("novaskin")
                break
            case _:
                print("Invalid choice.")

