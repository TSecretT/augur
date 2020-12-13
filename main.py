import time
import json
import database
import constants
from utils import *
from api import *
from proxy import *
import logging as lg

lg.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=lg.INFO)

proxies = []

db = database.Database('db.json')

def parse():
    lg.info("Parsing...")
    live_matches = getLiveMatches()
    lg.info(f"Current live matches: {len(live_matches)}")

    for i, match in enumerate(live_matches):
        start_time = time.time()

        # If match saved in db, skip
        if db.find(match['id']):
            lg.info(f"Match {match['id']} exists, skipping...")
            continue
        lg.info(f"[{i+1}/{len(live_matches)}] Parsing match {match['id']}")
        match = getMatchDetails(match['id'])
        players = getPlayersFromMatch(match)

        # Preset data
        data={}
        for team in players:
            data[team] = {}
            for MAP in constants.maps:
                data[team][MAP] = {}

        for team in players:
            for i, player_id in enumerate(players[team]):
                player_matches = getPlayerMatchesStats(player_id)
                player_matches = [convertMatchKeys(match) for match in player_matches]
                for MAP in constants.maps:
                    player_map_matches = filterMatchesByMap(player_matches, MAP)
                    player_stats = getAverageOfMatches(player_map_matches)
                    data[team][MAP][player_id] = player_stats

        # Get Average team stats
        for team in data:
            for MAP in data[team]:
                stats = [data[team][MAP][player_id] for player_id in data[team][MAP]]
                stats = getAverageOfMatches(stats)
                data[team][MAP] = stats
        # data should be as {faction1: {"mirage": {"Kills": 20}}, factio2: {...}}     

        match['prediction'] = predict(data, match['voting']['map']['pick'][0])
        match['data'] = data
        match['parsing_time'] = round(time.time() - start_time, 2)

        db.set_one(match['id'], match)
        lg.info(f"Match {match['id']} saved")
        time.sleep(10)

def check():
    lg.info("Checking matches...")
    # Get matches that were not checked yet from database
    unchecked_matches = db.filter('prediction_correct', None)
    for i, match in enumerate(unchecked_matches):
        start_time = time.time()
        lg.info(f"[{i+1}/{len(unchecked_matches)}] Checking match {match['id']}")
        match_with_result, winner = getMatchWinner(match['id'])
        if winner:
            match = {**match, **match_with_result}
            if match['prediction'] == 'tie':
                match['prediction_correct'] = getScoreDifference(match) < constants.TIE_SCORE_DIFFERENCE
            else:
                match['prediction_correct'] = match['prediction'] == winner
        match['checking_time'] = round(time.time() - start_time, 2)
        db.set_one(match['id'], match)
        lg.info(f"[{i+1}/{len(unchecked_matches)}] Match {match['id']} saved to database")

def main():
    while True:
        parse()
        check()
    
if __name__ == "__main__":
    main()