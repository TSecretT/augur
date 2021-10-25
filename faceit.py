import requests
import time
import constants
from multiprocessing import Pool

class Faceit():
    def __init__(self):
        self.session = requests.session()

    def get(self, url, data=None, params=None, proxies=None, headers=None, hit=1):
        try:
            res = requests.get(url, params=params, proxies=proxies, headers=headers)
            if res.status_code == 200:
                if proxies: print("Worked with proxy")
                return res.json()
            elif res.status_code == 429:
                raise requests.exceptions.ConnectionError
            elif res.status_code == 500:
                print(500, res.json())
            elif res.status_code == 404:
                return res
            else:
                return res
        except requests.exceptions.ConnectionError:
            print("Going too fast, sleeping for ", 10 * hit)
            time.sleep(10 * hit)
            return self.get(url, data=data, params=params, proxies=proxies, hit=hit+1)
        except requests.exceptions.ContentDecodingError:
            return self.get(url, data=data, params=params, headers=headers, proxies=proxies, hit=hit+1)
        except Exception as e:
            print("get error: ", e)

    def getMatches(self, offset: int=0, limit: int=100, region:str="EU", size:int=100, hub:bool=False, hub_id:str=None, page:bool=0, past:bool=False, full:bool=False):
        if hub and hub_id:
            params={
                "id": hub_id,
                "page": page,
                "size": limit,
                "type": "hub"
            }
            url = "https://api.faceit.com/match-history/v4/matches/competition"
        elif past:
            params={
                "id": "42e160fc-2651-4fa5-9a9b-829199e27adb",
                "page": page,
                "size": limit,
                "type": "matchmaking"
            }
            url = "https://api.faceit.com/match-history/v4/matches/competition"
        else:
            params = {
                "entityType": "matchmaking",
                "game": "csgo",
                "limit": limit,
                "offset": offset,
                "region": region,
                "state": constants.MATCHMAKING_STATES,
                "size": size
            }
            url = 'https://api.faceit.com/match/v1/matches/list'
        return self.get(url, params=params)['payload'] if not full else self.get(url, params=params)

    def getLiveMatches(self) -> list:
        """
            Returns the list of live matches
        """
        live_matches = []
        info = self.getMatches(full=True)
        total_pages = list(range(0, (info['totalPages'] + 1) * 100, 100))
        with Pool(8) as p:
            result_matches = p.map(self.getMatches, total_pages)
        for matches in result_matches:
            for match in matches:
                if match['state'] == "ONGOING":
                    live_matches.append(match)
        return live_matches

    # def getHubMatches(self, hub_id: str, page_start: int=0, page: int=0):
    #     """Returns the list of hub PAST matches"""
    #     hub_matches = []
    #     for i in range(page_start, page):
    #         matches = self.getMatches(hub=True, hub_id=hub_id, page=i)
    #         hub_matches.extend(matches)
    #     return hub_matches

    def getMatchDetails(self, id: str) -> object:
        """Get match details"""
        return self.get(f"https://api.faceit.com/match/v2/match/{id}")['payload']

    # def getPlayerMatches(self, id: str, from_time=constants.DEFAULT_FROM, to_time=constants.DEFAULT_TO, page=0, size=100, offset=0):
    #     ? code 403
    #     """ Returns list of match objects within time period """
    #     params = {
    #         "from": from_time,
    #         "to": to_time,
    #         "page": page,
    #         "size": size,
    #         "offset": offset
    #     }
        
    #     return self.get(f"https://api.faceit.com/match-history/v5/players/{id}/history", params=params)

    def getPlayerMatchesStats(self, id: str, page:int=0, size:int=100) -> list:
        """Return list of objects of stats"""
        params = {
            "page": page,
            "size": size,
        }
        return self.get(f"https://api.faceit.com/stats/v1/stats/time/users/{id}/games/csgo", params=params)

    def getPlayerStats(self, id:str) -> object:
        return self.get(f"https://api.faceit.com/stats/v1/stats/users/{id}/games/csgo")

    def getMatchWinner(self, id: str):
        """ Returns "faction1" or "faction2" or None if no result """
        match = self.getMatchDetails(id)
        if match['status'] == "FINISHED":
            match_stats = self.getMatchStats(id)
            match['score'] = match_stats['i18']
            return match, match['results'][0]['winner']
        else:
            return {}, None
        
    def getMatchStats(self, id: str) -> object:
        """Returns the scoreboard of the match"""
        res = self.get(f'https://api.faceit.com/stats/v1/stats/matches/{id}')
        return res[0] if len(res) > 0 else None

    def getPlayerInfo(self, nickname: str):
        return self.get(f"https://api.faceit.com/core/v1/nicknames/{nickname}")