import time
import json
import database
import constants
import config
from utils import *
from api import *
from proxy import *
import logging as lg
from multiprocessing import Pool
from pymongo import BulkWriteError

lg.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=lg.INFO)

proxies = []

# db = database.Database('db.json')
db = database.Mongo().db

def scanMatch(match):
    start_time = time.time()
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
    match['parsed_at'] = time.time()
    match['parsing_time'] = round(time.time() - start_time, 2)
    match = stripMatch(match)
    return match

def parse():
    start_time = time.time()
    lg.info("Parsing...")
    live_matches = getLiveMatches()
    lg.info(f"Current live matches: {len(live_matches)}")

    for offset in range(config.MATCH_PARSE_OFFSET, len(live_matches) + config.MATCH_PARSE_OFFSET, config.MATCH_PARSE_OFFSET):
        lg.info(f"Parsing offset {offset}")
        matches = live_matches[offset-config.MATCH_PARSE_OFFSET:offset]
        with Pool(8) as p:
            matches = p.map(scanMatch, matches)
        db_start_time = time.time()
        ids = [{'_id': match['id']} for match in matches]
        saved_matches = db.find({"$or": ids})
        saved_matches = [match['id'] for match in saved_matches]
        matches = [match for match in matches if match['id'] not in saved_matches]
        try:
            db.insert_many(matches)
        except BulkWriteError:
            pass
    time_took = round(time.time() - start_time, 2)
    print(f"Finished scan of {len(live_matches)} matches in {time_took}, saved in {round(time.time() - db_start_time, 2)} [{round(time_took / len(live_matches), 2)} s/match]")

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


def databaza():
    mydict = { "_id": "1231", "name": "John", "address": "Highway 37" }
    x = db.insert_one(mydict)

def main():
    while True:
        parse()
        # check()
    
if __name__ == "__main__":
    main()