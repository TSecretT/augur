import api
import constants
import database
import proxy
import config
import utils
import time
from multiprocessing import Pool

db = database.Mongo().db

def scanMatch(match):
    start_time = time.time()
    match = api.getMatchDetails(match['id'])
    players = utils.getPlayersFromMatch(match)

    # Preset data
    data={}
    for team in players:
        data[team] = {}
        for MAP in constants.maps:
            data[team][MAP] = {}

    for team in players:
        for i, player_id in enumerate(players[team]):
            player_matches = api.getPlayerMatchesStats(player_id)
            player_matches = [utils.convertMatchKeys(match) for match in player_matches]
            for MAP in constants.maps:
                player_map_matches = utils.filterMatchesByMap(player_matches, MAP)
                player_stats = utils.getAverageOfMatches(player_map_matches)
                data[team][MAP][player_id] = player_stats

    # Get Average team stats
    for team in data:
        for MAP in data[team]:
            stats = [data[team][MAP][player_id] for player_id in data[team][MAP]]
            stats = utils.getAverageOfMatches(stats)
            data[team][MAP] = stats
    # data should be as {faction1: {"mirage": {"Kills": 20}}, factio2: {...}}     

    match['prediction'] = utils.predict(data, match['voting']['map']['pick'][0])
    match['data'] = data
    match['parsing_time'] = round(time.time() - start_time, 2)

    print('\n')
    print(match['prediction'])
    print("Finished in", round(time.time() - start_time, 2))
    return match

def checkMatch(match):
    start_time = time.time()
    match_with_result, winner = api.getMatchWinner(match['id'])
    if winner:
        match = {**match, **match_with_result}
        if match['prediction'] == 'tie':
            match['prediction_correct'] = utils.getScoreDifference(match) < constants.TIE_SCORE_DIFFERENCE
        else:
            match['prediction_correct'] = match['prediction'] == winner
    match['checking_time'] = round(time.time() - start_time, 2)
    match = utils.stripMatch(match)
    return match

def check():
    print("Loading unchecked matches...")
    matches = db.find({'prediction_correct': None})
    matches = [match for match in matches]
    for offset in list(range( config.MATCH_CHECK_OFFSET, len(matches) + config.MATCH_CHECK_OFFSET, config.MATCH_CHECK_OFFSET )):
        print("Parsing offset", offset)
        offset_time_start = time.time()
        try:
            with Pool(8) as p:
                checked_matches = p.map(checkMatch, matches[offset - config.MATCH_CHECK_OFFSET : offset])
            for match in checked_matches:
                db.replace_one({"_id": match['id']}, {**match}, True)
            duration = round(time.time() - offset_time_start, 2)
            print(f"Finished offset {offset} in {duration} [{round(duration / config.MATCH_CHECK_OFFSET, 2)}]")
        except:
            pass

def statistics():
    matches = db.find({"prediction_correct": {"$exists": True}})
    matches = [match for match in matches]
    correct_predictions = 0
    average_parsing_time = []
    average_checking_time = []
    for match in matches:
        if match['prediction_correct']: correct_predictions+=1
        average_parsing_time.append(match['parsing_time'])
        average_checking_time.append(match['checking_time'])

    average_parsing_time = utils.average(average_parsing_time)
    average_checking_time = utils.average(average_checking_time)
    print(f"Total matches: {len(matches)}\nPrediction rate: {round(correct_predictions / len(matches), 2)*100}\nAvg. parsing time: {average_parsing_time}\nAvg.checking time:{average_checking_time}")

if __name__ == '__main__':
    check()