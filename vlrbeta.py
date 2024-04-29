import time
import re

from bs4 import BeautifulSoup as bs
import requests

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

from xml_grabber import XML_links

xlinks = XML_links('https://www.vlr.gg/312779/gen-g-vs-sentinels-champions-tour-2024-masters-madrid-gf/?game=all&tab=overview')


class Match:
    def __init__(self, link, XML_links):

        self.top_name = XML_links.xpaths["top"]["name"]
        self.bot_name = XML_links.xpaths["bottom"]["name"]
        self.top_acs = XML_links.xpaths["top"]["acs"]
        self.bot_acs = XML_links.xpaths["bottom"]["acs"]
        self.top_agent = XML_links.xpaths["top"]["agent"]
        self.bot_agent = XML_links.xpaths["bottom"]["agent"]
        self.top_url = XML_links.xpaths["top"]["url"]
        self.bot_url = XML_links.xpaths["bottom"]["url"]
        self.top_rating = XML_links.xpaths["top"]["rating"]
        self.bot_rating = XML_links.xpaths["bottom"]["rating"]
        self.top_kills = XML_links.xpaths["top"]["kills"]
        self.bot_kills = XML_links.xpaths["bottom"]["kills"]
        self.top_kills = XML_links.xpaths["top"]["kills"]
        self.bot_kills = XML_links.xpaths["bottom"]["kills"]
        self.top_deaths = XML_links.xpaths["top"]["deaths"]
        self.bot_deaths = XML_links.xpaths["bottom"]["deaths"]
        self.top_assists = XML_links.xpaths["top"]["assists"]
        self.bot_assists = XML_links.xpaths["bottom"]["assists"]
        self.top_pm = XML_links.xpaths["top"]["pm"]
        self.bot_pm = XML_links.xpaths["bottom"]["pm"]
        self.top_hsp = XML_links.xpaths["top"]["hsp"]
        self.bot_hsp = XML_links.xpaths["bottom"]["hsp"]


        self.link = link
        self.match = self.requester(link)

    @staticmethod
    def requester(url):
        htmlText = requests.get(url)
        return bs(htmlText.content, "lxml")

    def get_team_logo_hl(self, url):

        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in headless mode
        chrome_options.add_argument("window-size=1920,1080")
        chrome_options.add_argument("start-maximized")
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")
        chrome_options.add_argument("--log-level=3")

        s = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=s, options=chrome_options)

        # Navigate to the website
        driver.get(url)

        # Wait for the dark mode switch to be clickable and click it
        wait = WebDriverWait(driver, 20)  # Wait up to 20 seconds
        dark_mode_switch = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'body > header > nav > div.header-switch.js-dark-switch')))
        dark_mode_switch.click()

        time.sleep(1)

        driver.refresh()
        # Now the website should be in dark mode, and you can scrape it as needed
        logo_link = wait.until(EC.presence_of_element_located(
            (By.XPATH, '/html/body/div[5]/div[1]/div/div[1]/div[1]/div[1]/div/img'))).get_attribute('src')
        
        # Don't forget to close the driver when you're done
        driver.quit()
        

        return logo_link

    def get_team_info(self, mod):
        team_url = 'https://www.vlr.gg' + self.match.find('a', class_=f"match-header-link wf-link-hover mod-{mod}")['href']
        team_link = self.requester(team_url)
        team_name = team_link.find('h1', class_='wf-title').text.strip()
        try:
            twitter = team_link.find('div', class_='team-header-links').text.lstrip()
            twitter = '@' + twitter.replace('\n', '').replace('\t', '').split('@')[1].split(' ')[0]
        except:
            twitter = None

        try:
            logo_link = self.get_team_logo_hl(team_url)
        except:
            logo_link = team_link.find('div', class_='wf-avatar team-header-logo').find('img')['src']
            if logo_link.startswith('//'):
                logo_link = 'https:' + logo_link
            elif logo_link == '/img/vlr/tmp/vlr.png':
                logo_link = 'https://www.vlr.gg/img/vlr/tmp/vlr.png'

        return team_name, twitter, logo_link

    def map(self):
        maps = [i.span.text.strip().replace('\n', '').replace('\t', '').replace('PICK', '') for i in self.match.find_all('div', class_='map')]
        return maps

    def event(self):
        event = self.match.find('div', style='font-weight: 700;').text.strip()
        return event.replace('\n', '').replace('\t', '')

    def round(self):
        round = self.match.find('div', class_='match-header-event-series').text.strip()
        return round.replace('\n', '').replace('\t', '')

    def scores(self):
        return [i.text.strip() for i in self.match.find_all('div', class_='score')]

    def leftteam(self):
        left_team_name, _, _ = self.get_team_info(1)
        return left_team_name

    def lefttwitter(self):
        _, left_twitter, _ = self.get_team_info(1)
        return left_twitter

    def righttwitter(self):
        _, right_twitter, _ = self.get_team_info(2)
        return right_twitter

    def rightteam(self):
        right_team_name, _, _ = self.get_team_info(2)
        return right_team_name

    def mapscore(self):
        mapscore = []
        maps = self.map()
        score = self.scores()
        for i in range(len(maps)):
            mapscore.append((maps[i], score[i*2:i*2+2]))
        return mapscore

    def get_mvp(self):
     
        if float(self.top_rating) > float(self.bot_rating):

            playername = self.top_name
            mvpacs = self.top_acs
            agent = self.top_agent
            pfp_link = self.top_url
            hsp = self.top_hsp
            pm = self.top_pm
            kills = self.top_kills
            deaths = self.top_deaths
            assists = self.top_assists

        else:

            playername = self.bot_name
            mvpacs = self.bot_acs
            agent = self.bot_agent
            pfp_link = self.bot_url
            hsp = self.bot_hsp
            pm = self.bot_pm
            kills = self.bot_kills
            deaths = self.bot_deaths
            assists = self.bot_assists

        player = self.requester(self.top_url)
        pfp_link = player.find('div', class_='wf-avatar mod-player').find('img')['src']
        if pfp_link.startswith('//'):
            pfp_link = 'https:' + pfp_link
        elif pfp_link == "/img/base/ph/sil.png":
            pfp_link = 'https://www.vlr.gg/img/base/ph/sil.png'
        return {'player_name': playername, 'mvp_acs': mvpacs, 'agent': agent, 'image': pfp_link, 'hsp': hsp, 'pm': pm, 'kills': kills, 'deaths': deaths, 'assists': assists}

    def __str__(self):
        output = ""
        s = self.mapscore()
        rightteam = self.rightteam()
        leftteam = self.leftteam()
        map = self.map()
        ltwitter = self.lefttwitter()
        rtwitter = self.righttwitter()
        lwinner, rwinner = 0, 0
        for i in range(len(s)):
            if int(s[i][1][0]) > int(s[i][1][1]):
                output += f"{leftteam} defeat {rightteam} {s[i][1][0]} to {s[i][1][1]} on {map[i]}.\n"
                lwinner += 1
            else:
                output += f"{rightteam} defeat {leftteam} {s[i][1][1]} to {s[i][1][0]} on {map[i]}.\n"
                rwinner += 1
        winner = f"{ltwitter or leftteam} {lwinner}-{rwinner} {rtwitter or rightteam}"
        final_score = f"{self.event()} {self.round()}\n{winner.lstrip()}\n{output}"
        return final_score if len(final_score) <= 280 else f"{self.event()} {self.round()}\n\n{winner.lstrip()}\n\n{output}"

#m = Match("https://www.vlr.gg/336088/shopify-rebellion-vs-misu-s-qts-game-changers-2024-north-america-series-2-sf")


class MatchInfo:
    def __init__(self, match):
        self.event_name = match.event()
        self.round = match.round()

        team1_name, team1_twitter, team1_logo = match.get_team_info(1)
        team2_name, team2_twitter, team2_logo = match.get_team_info(2)

        self.team_info = {
            team1_name: {'twitter': team1_twitter, 'logo': team1_logo, 'maps_won': 0},
            team2_name: {'twitter': team2_twitter, 'logo': team2_logo, 'maps_won': 0}
        }

        self.map_info = {}  # Initialize map_info as an empty dictionary
        for map_name, scores in match.mapscore():
            winner = team1_name if int(scores[0]) > int(scores[1]) else team2_name
            self.team_info[winner]['maps_won'] += 1
            self.map_info[map_name] = {'score': scores, 'winner': winner}  # Add map information to map_info
        self.mvp_info = match.get_mvp()

    def __str__(self):
        team1_name, team1_info = list(self.team_info.items())[0]
        team2_name, team2_info = list(self.team_info.items())[1]
        return f"{team1_info['twitter'] or team1_name} {team1_info['maps_won']}-{team2_info['maps_won']} {team2_info['twitter'] or team2_name}"

def live_matches():
    match = requester('https://www.vlr.gg/matches')
    m1 = match.find_all('div', class_='wf-card')
    matchlist = ['https://www.vlr.gg' + s['href'] for i in m1 for s in i.find_all('a')]
    matchlist = matchlist[2:]  # Remove the first two elements

    # loop until you find 1 game that isn't live then break
    # all live games are going to be at the top so no point in looping through 32 games if only 1 is live
    livelist = []
    for match_url in matchlist:
        game = requester(match_url)
        if game.find('div', class_='match-header-vs-note').text.strip() == 'live':
            livelist.append(match_url)
        else:
            break
    return livelist

def is_completed(matchurl):
    game = requester(matchurl)
    return game.find('div', class_='match-header-vs-note').text.strip() == 'final'
def requester(url):
  htmlText = requests.get(url)
  return bs(htmlText.content, "lxml")

#print(live_matches())

#m = Match('https://www.vlr.gg/324469/kpi-gaming-vs-case-esports-challengers-league-2024-spain-rising-split-1-playoffs-gf')
#mi = MatchInfo(m)

