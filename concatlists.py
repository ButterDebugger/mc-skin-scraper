from os.path import exists

filename = input("Filename of list: ")

if not exists(filename):
    print("File doesn't exist!")
    quit()

with open(filename, "r") as f:
    text = f.read()

with open("uuids.txt", "a") as f:
    f.write("\n" + text)