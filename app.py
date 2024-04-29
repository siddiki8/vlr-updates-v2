import vlrbeta as vlr
import handler
import time
from keep_alive import keep_alive

t = handler.Tweet()
def main():
    live_list = []
    while True:
        clist = []
        matchlist = vlr.live_matches()      # Get list of live matches

        for match in matchlist:             # Iterate through list of live matches and add to live_list if not already in it
            if match not in live_list:
                live_list.append(i)

        for match in live_list:           # Iterate through live_list and check if match is completed
            if vlr.is_completed(match) == True:
                live_list.remove(match)   # If match is completed, remove from live_list
                clist.append(match)       # Add match to list of completed matches

        for i in clist:                # Iterate through list of completed matches
            t.tweet_match(i)  # Tweet completed match
        time.sleep(60)

if __name__ == "__main__":
    keep_alive()
    main()