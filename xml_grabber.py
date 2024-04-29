import requests
from lxml import html
import json
import re


def get_stats(link):

    page_link = requests.get(link)

    with open('xpaths.json') as json_file:
        xpaths = json.load(json_file)
        
    page_html = html.fromstring(page_link.content)

    topnbot = ["top", "bottom"]
    for toporbot in topnbot:
        for name in xpaths[toporbot]:

            addresses = page_html.xpath(xpaths[toporbot][name])

            if name == 'agent':
               
                for address in addresses:
                    element2 = re.sub("[\t]","", address.__str__())
                    element3 = re.sub("[\n]","", element2)
                    element4 = re.sub("[ ]","", element3)
                    xpaths[toporbot][name] = re.sub("[\t]","", element4) 

            elif name == 'url':

                for address in addresses:
                    element2 = re.sub("[\t]","", address.__str__())
                    element3 = re.sub("[\n]","", element2)
                    element4 = re.sub("[ ]","", element3)
                    xpaths[toporbot][name] = "https://www.vlr.gg" + re.sub("[\t]","", element4)
                    
            else:

                for address in addresses:
                    element2 = re.sub("[\t]","", address.text)
                    element3 = re.sub("[\n]","", element2)
                    element4 = re.sub("[ ]","", element3)
                    xpaths[toporbot][name] = re.sub("[\t]","", element4)

    
    return xpaths

