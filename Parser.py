import requests
import time
import json
from bs4 import BeautifulSoup
import base64
import pymongo
from config import config



client = pymongo.MongoClient(config['mongoDB_url'])
db = client['faceit']['matches']

hub_id = "8d2b1481-6bb6-44cd-81d5-c79a11c76fae"


def getHubInfo(id):
    return requests.get('https://api.faceit.com/hubs/v1/hub/8d2b1481-6bb6-44cd-81d5-c79a11c76fae').json()


def getHubMatches(page):
    params = {
        "id": "8d2b1481-6bb6-44cd-81d5-c79a11c76fae",
        "page": page,
        "size": 100,
        "type": "hub"
    }
    return get('https://api.faceit.com/match-history/v4/matches/competition', params)['payload']



def getPlayerMatches(id):
    params={
        "size": 100,
        "page": 0
    }
    return get(f"https://api.faceit.com/stats/v1/stats/time/users/{id}/games/csgo", params)


def getProxyList():
    soup = BeautifulSoup(requests.get('http://free-proxy.cz/en/proxylist/country/all/https/ping/level1').content, "lxml")
    rows = soup.find('table', id="proxy_list").find('tbody').findAll('tr')
    ips = []
    for row in rows:
        tds = row.findAll('td')
        try:
            coded = tds[0].text.strip()[30:][:-3]
            ip = base64.b64decode(coded).decode('utf-8')

            port = tds[1].text

            type_ = tds[2].text
    #         if type_ != "HTTPS": continue

            ips.append({ "https:": f"https://{ip}:{port}" })
        except:
            pass

    return ips

def get(url, params=None, proxies=None):
    tries = 1
    while True:
        res = requests.get(url, params=params, proxies=proxies)
        if res and res.status_code == 200:
            return res.json()
        elif res:
            print(f"Get error {res.status_code}")
        else:
            print("Get unknown error")
        print("Sleeping for", tries * 10)
        time.sleep(tries + 10)
        tries+=1

def parse(startPage=None, endPage=None):
    for page in range(450, 0, -1):
        print("======= Page", page, "=========")
        matches = getHubMatches(page)
        for i, match in enumerate(matches):
            print(f"Match {i+1}/{len(matches)}")
            saved_match = db.find_one({"matchId" : match['matchId']})
            if saved_match: print(f"Match {i} already exists, skipping")
            for i in range(1,3):
                players = match['teams'][f"faction{i}"]['roster']
                for j, player in enumerate(players):
                    matches = getPlayerMatches(player['id'])
                    match['teams'][f"faction{i}"]['roster'][j]['matches'] = matches
            _ = db.insert_one(match)

parse()