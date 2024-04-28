import time
import vlrbeta
from keep_alive import keep_alive
def get_live_matches(live_set):
    matchlist = vlrbeta.live_matches()
    print("Current live matches: ")
    print(matchlist)
    for match_url in matchlist:
        live_set.add(match_url)
    return live_set

def get_completed_matches(live_set):
    live_set = {match_url for match_url in live_set if not vlrbeta.is_completed(match_url)}
    clist = [match_url for match_url in live_set if vlrbeta.is_completed(match_url)]
    print("Current completed matches: ")
    print(clist)
    return clist

def process_completed_matches(clist):
    for match_url in clist:
        match = vlrbeta.Match(match_url)
        match_info = vlrbeta.MatchInfo(match)
        print(str(match_info) + " has ended")

def main():
    live_set = set()
    while True:
        try:
            live_set = get_live_matches(live_set)
            clist = get_completed_matches(live_set)
            process_completed_matches(clist)
            print("Zzz...")
            time.sleep(60)
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    keep_alive()
    main()