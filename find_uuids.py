from from_names import find_by_names
from namemc_hearts import grab_likers
from os import makedirs
from os.path import exists

if not exists("./uuids"):
    makedirs("./uuids")

while True:
    print("[1] Randomly generated usernames to uuids")
    print("[2] Grab uuids from players who heart minecraft servers on NameMC")

    choice = input("> ")

    if choice == "1":
        find_by_names()
        break
    elif choice == "2":
        grab_likers()
        break
    else:
        print()
        print("Invalid option. Please try again")
        print()
