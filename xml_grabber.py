import requests
from lxml import html
import json
import re

class XML_links:

    def __init__(self, link):

        page_link = requests.get(link)

        with open('xpaths.json') as json_file:
            self.xpaths = json.load(json_file)
        
        self.page_html = html.fromstring(page_link.content)

        for name in self.xpaths["top"]:

            addresses = self.page_html.xpath(self.xpaths["top"][name])

            if name == 'agent':
               
               for address in addresses:
                    element2 = re.sub("[\t]","", address.__str__())
                    element3 = re.sub("[\n]","", element2)
                    element4 = re.sub("[ ]","", element3)
                    self.xpaths["top"][name] = re.sub("[\t]","", element4) 

            elif name == 'url':

                for address in addresses:
                    element2 = re.sub("[\t]","", address.__str__())
                    element3 = re.sub("[\n]","", element2)
                    element4 = re.sub("[ ]","", element3)
                    self.xpaths["top"][name] = "https://www.vlr.gg" + re.sub("[\t]","", element4)
                    
            else:

                for address in addresses:
                    element2 = re.sub("[\t]","", address.text)
                    element3 = re.sub("[\n]","", element2)
                    element4 = re.sub("[ ]","", element3)
                    self.xpaths["top"][name] = re.sub("[\t]","", element4)

        for name in self.xpaths["bottom"]:

            addresses = self.page_html.xpath(self.xpaths["bottom"][name])

            if name == 'agent':
               
               for address in addresses:
                    element2 = re.sub("[\t]","", address.__str__())
                    element3 = re.sub("[\n]","", element2)
                    element4 = re.sub("[ ]","", element3)
                    self.xpaths["bottom"][name] = re.sub("[\t]","", element4) 
                    

            elif name == 'url':

                for address in addresses:
                    element2 = re.sub("[\t]","", address.__str__())
                    element3 = re.sub("[\n]","", element2)
                    element4 = re.sub("[ ]","", element3)
                    self.xpaths["bottom"][name] = "https://www.vlr.gg" + re.sub("[\t]","", element4)

            else:

                for address in addresses:
                    element2 = re.sub("[\t]","", address.text)
                    element3 = re.sub("[\n]","", element2)
                    element4 = re.sub("[ ]","", element3)
                    self.xpaths["bottom"][name] = re.sub("[\t]","", element4)

    
        

#x = XML_links('https://www.vlr.gg/312779/gen-g-vs-sentinels-champions-tour-2024-masters-madrid-gf/?game=162351&tab=overview')

#print(x.xpaths['top']['name'])
#print(x.xpaths)

#//*[@id=\"wrapper\"]/div[1]/div[3]/div[6]/div/div[3]/div[1]/div[3]/div[2]/table/tbody/tr[1]/td[2]/div/span/img
#//*[@id="wrapper"]/div[1]/div[3]/div[6]/div/div[3]/div[2]/div[2]/div[2]/table/tbody/tr[1]/td[2]/div/span[1]/img


# Parse the content of the request with lxml
#tree = html.fromstring(r.content)

# Use xpath to find the item
# Replace 'your_xpath_here' with your actual XPath
#top_dude = tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[2]/div[2]/div[1]/table/tbody/tr[1]/td[3]/span/span[1]')
#bottom_dude = tree.xpath('/html/body/div[5]/div[1]/div[3]/div[6]/div/div[3]/div[2]/div[2]/div[2]/table/tbody/tr[1]/td[3]/span/span[1]')

#top_acs = tree.xpath('//*[@id="wrapper"]/div[1]/div[3]/div[6]/div/div[3]/div[1]/div[3]/div[1]/table/tbody/tr[1]/td[4]/span/span[1]')

#for element in top_dude:
    #print(element.text)

#for element in bottom_dude:
    #print(element.text)

#for element in top_acs:
    #print(element.text)