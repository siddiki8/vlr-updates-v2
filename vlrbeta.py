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
from xml_grabber import get_stats

class Match:
    def __init__(self, link):
        self.link = link
        self.match = self.requester(link)
        self.team_info = {
            'team1': self.get_team_info(1),
            'team2': self.get_team_info(2)
        }
        self.map_info = self.mapscore()
        self.mvp_info = self.get_mvp()
        self.event = self.event()
        self.round = self.round()

    @staticmethod
    def requester(url):
        htmlText = requests.get(url)
        return bs(htmlText.content, "lxml")

    def map(self):
        maps = [i.span.text.strip().replace('\n', '').replace('\t', '').replace('PICK', '') for i in
                self.match.find_all('div', class_='map')]
        return maps

    def event(self):
        event = self.match.find('div', style='font-weight: 700;').text.strip()
        return event.replace('\n', '').replace('\t', '')

    def round(self):
        round = self.match.find('div', class_='match-header-event-series').text.strip()
        return round.replace('\n', '').replace('\t', '')

    def scores(self):
        return [i.text.strip() for i in self.match.find_all('div', class_='score')]

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
        team_url = 'https://www.vlr.gg' + self.match.find('a', class_=f"match-header-link wf-link-hover mod-{mod}")[
            'href']
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

        return {"team_name": team_name, "twitter": twitter, "logo": logo_link}


    def mapscore(self):
        map_info = {}  # Initialize map_info as an empty dictionary
        maps = self.map()
        score = self.scores()
        for i in range(len(maps)):
            winner = self.team_info['team1']['team_name'] if int(score[i*2]) > int(score[i*2+1]) else self.team_info['team2']['team_name']
            map_info[maps[i]] = {'score': score[i*2:i*2+2], 'winner': winner}  # Add map information to map_info

        # Update team_info with maps won
        self.team_info['team1']['maps_won'] = sum(1 for map_info in map_info.values() if map_info['winner'] == self.team_info['team1']['team_name'])
        self.team_info['team2']['maps_won'] = sum(1 for map_info in map_info.values() if map_info['winner'] == self.team_info['team2']['team_name'])

        return map_info

    def get_mvp(self):
        dictionary = get_stats(self.link)
    
        if float(dictionary["top"]["rating"]) > float(dictionary["bottom"]["rating"]):
            mvp_loc = 'top'
        else:
            mvp_loc = 'bottom'
        
        player = self.requester(dictionary[mvp_loc]['url'])
        pfp_link = player.find('div', class_='wf-avatar mod-player').find('img')['src']
        if pfp_link.startswith('//'):
            pfp_link = 'https:' + pfp_link
        elif pfp_link == "/img/base/ph/sil.png":
            pfp_link = 'https://www.vlr.gg/img/base/ph/sil.png'
        
        try:
            mvptwitter = player.find('a',style="margin-top: 3px; display: block;").text.lstrip()
        except:
            mvptwitter = None

            
        dictionary[mvp_loc]['url'] = pfp_link
        dictionary[mvp_loc]['twitter'] = mvptwitter
        dictionary[mvp_loc]['player_name'] = dictionary[mvp_loc]['player']
        
        return dictionary[mvp_loc]

    def __str__(self):
        event_name = self.event
        round_name = self.round
        team1_twitter = self.team_info['team1']['twitter'] or self.team_info['team1']['team_name']
        team2_twitter = self.team_info['team2']['twitter'] or self.team_info['team2']['team_name']
        team1_maps_won = self.team_info['team1']['maps_won']
        team2_maps_won = self.team_info['team2']['maps_won']
        mvp_twitter = self.mvp_info['twitter'] or self.mvp_info['player_name']

        return f"{event_name} ({round_name})\n{team1_twitter} {team1_maps_won} - {team2_maps_won} {team2_twitter}\nMVP: {mvp_twitter}"

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