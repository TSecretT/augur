import api
import constants
import database
import utils
import time
from multiprocessing import Pool

db = database.Database('./db.json')

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

if __name__ == '__main__':
    n = 100
    start_time = time.time()
    matches = db.get(as_list=True)[:n]
    matches = [match['id'] for match in matches]
    with Pool(8) as p:
        matches = p.map(api.getMatchDetails, matches)
    
    with Pool(8) as p:
        matches = p.map(scanMatch, matches)
    time_took = round(time.time() - start_time, 2)
    print(f"Finished scan of {n} matches in {time_took} [{round(time_took / n, 2)} s/match]")

    parsing_time = [match['parsing_time'] for match in matches]
    print(utils.average(parsing_time))
