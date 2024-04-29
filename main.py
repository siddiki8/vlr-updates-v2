import vlr
import twitter
import time
from keep_alive import keep_alive

# keeps the script running on a thread
keep_alive()

live_list = []
while True:
  clist = []
  matchlist = vlr.live_matches()
  for i in matchlist:
    if i not in live_list:
      live_list.append(i)
    else:
      pass
  for i in live_list:
    if vlr.is_completed(i) == True:
      live_list.remove(i)
      clist.append(i)
    else:
      pass
  for i in clist:
    twitter.tweet(str(vlr.Match(i)))
  clist = []
  time.sleep(60)