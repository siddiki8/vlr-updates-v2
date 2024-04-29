import time
import vlrbeta
from keep_alive import keep_alive

def get_live_matches(live_set):
    matchlist = vlrbeta.live_matches()
    for match_url in matchlist:
        live_set.add(match_url)
    return live_set

def get_completed_matches(live_set):
    clist = [match_url for match_url in live_set if vlrbeta.is_completed(match_url)]
    #print("Current completed matches: ")
    #print(clist)
    return clist

def process_completed_matches(clist):
    for match_url in clist:
        match = vlrbeta.Match(match_url)
        print(str(match) + "/n has ended!")

def main():
    live_set = set()
    while True:
        try:
            live_set = get_live_matches(live_set)
            print("These are the current live matches! I'll check if any of them finished in a minute.")
            print(live_set)
            for _ in range(60):  # Loop for 60 seconds
                print("Zzz...", end="\r", flush=True)  # Print "Zzz..." and return to the start of the line
                time.sleep(1)  # Sleep for 1 second
            clist = get_completed_matches(live_set)
            if len(clist) > 0:
                print("The following matches finished in the last minute: ")
                print(clist)
                print("Processing completed matches...")
                process_completed_matches(clist)
            else:
                print("No matches have finished in the last minute.")
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    keep_alive()
    main()