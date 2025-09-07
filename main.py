if __name__ == "__main__":
    print("[1] Find UUIDs by generating usernames")

    print("[2] Find UUIDs by scanning likes from NameMC")

    print("[3] Get skins from UUIDs")
    print("\tScans through every uuid lists and converts uuids to skins")

    print("[4] Listing search")
    print("\tUsed to get skins published onto Minecraft skin gallery websites")

    print("[5] Clean UUIDs")
    print("\tUsed to filter out duplicates and reformats all uuid lists")

    try:
        while True:
            match input("> "):
                case "1":
                    from from_names import find_by_names

                    find_by_names()
                    break
                case "2":
                    from namemc_hearts import grab_likers

                    grab_likers()
                    break
                case "3":
                    from get_skins import main

                    main()
                    break
                case "4":
                    from listing import main

                    main()
                    break
                case "5":
                    from clean_uuids import main

                    main()
                    break
                case _:
                    print("Invalid option.")
    except KeyboardInterrupt:
        print("Process exited.")
