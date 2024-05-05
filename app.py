import vlrbeta as vlr
import handler
import time

t = handler.Tweet()
def main():
    live_list = []
    while True:
        try:
            clist = []
            matchlist = vlr.live_matches()      # Get list of live matches
            print("These are the current live matches: ", matchlist)

            for match in matchlist:             # Iterate through list of live matches and add to live_list if not already in it
                if match not in live_list:
                    live_list.append(match)

            for match in live_list:           # Iterate through live_list and check if match is completed
                if vlr.is_completed(match) == True:
                    live_list.remove(match)   # If match is completed, remove from live_list
                    clist.append(match)       # Add match to list of completed matches

            if len(clist) == 0:
                print("No matches completed")
            else:
                print("These matches have completed: ", clist)

            for match in clist:                # Iterate through list of completed matches
                try:
                    print("tweeting match: " + match)
                    t.tweet_match(match)  # Tweet completed match
                    print("Tweeted match: " + match)
                except Exception as e:
                    print("Error tweeting match: " + match)
                    print(e)
        except Exception as e:
            print("Error in main loop")
            print(e)

        print("Sleeping for 60 seconds")
        print("Zzz...")
        time.sleep(60)

if __name__ == "__main__":
    main()