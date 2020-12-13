import requests
import json
import time
from proxy import *
import constants

proxies = []

def get(url, data=None, params=None, proxies=None, headers=None, hit=1):
    res = requests.get(url, params=params, proxies=proxies, headers=headers)
    
    if res.status_code == 200:
        return res.json()
    elif res.status_code == 429:
        print("Going too fast, switching proxy")
        removeProxy(proxies)
        proxy = getProxy(proxies)
        print(f"Switched to {proxy['https']}")
#         print("Going too fase, sleeping for", hit * 5)
#         time.sleep(hit * 5)
        return get(url, data=data, params=params, proxies=proxies, hit=hit+1)
    elif res.status_code == 500:
        print(500, res.json())
    else:
        print(res.status_code)

def getMatches(limit=100, region="EU", offset=0, hub=False, hub_id=None, page=0):
    if(hub and hub_id):
        params={
            "id": hub_id,
            "page": page,
            "size": limit,
            "type": "hub"
        }
        url = "https://api.faceit.com/match-history/v4/matches/competition"
    else:
        params = {
            "entityType": "matchmaking",
            "game": "csgo",
            "limit": limit,
            "offset": offset,
            "region": region,
            "state": constants.MATCHMAKING_STATES
        }
        url = 'https://api.faceit.com/match/v1/matches/list'
    return get(url, params=params)['payload']

# Returns the list of current live matches
def getLiveMatches() -> list:
    live_matches = []
    offset = 0
    while offset < 200:
        matches = getMatches(offset=offset)
        if not matches: return live_matches
        for match in matches:
            if match['state'] == "ONGOING":
                live_matches.append(match)
        offset+= 100
        print(offset)
    return live_matches

# Returns the list of hub PAST matches
def getHubMatches(page_start=0, page=10):
    hub_matches = []
    for i in range(page_start, page):
        print(f"Page {i+1}")
        matches = getMatches(hub=True, hub_id="74624044-158f-446a-ad4f-cbd2e0e89423", page=i)
        hub_matches.extend(matches)
    return hub_matches

# Get match details
def getMatchDetails(id: str) -> object:
    return get(f"https://api.faceit.com/match/v2/match/{id}")['payload']

# Returns list of match objects within time period 
def getPlayerMatches(id: str, from_time=constants.DEFAULT_FROM, to_time=constants.DEFAULT_TO, page=0, size=100, offset=0):
    params = {
        "from": from_time,
        "to": to_time,
        "page": page,
        "size": size,
        "offset": offset
    }
    
    headers={
        "authorization": "Bearer 6c86f4d6-df61-484a-b8d2-369f9b0521bc"
    }
    
    return get(f"https://api.faceit.com/match-history/v5/players/{id}/history", params=params, headers=headers)['payload']

# Return list of objects of stats
def getPlayerMatchesStats(id: str, page=0, size=100) -> list:
    params = {
        "page": page,
        "size": size,
    }
    return get(f"https://api.faceit.com/stats/v1/stats/time/users/{id}/games/csgo", params=params)