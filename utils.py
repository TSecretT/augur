import constants

# Convert keys like "s1", "s2" to human readable "Kills", "Assists"
def convertMatchKeys(match: object) -> object:
    copy_match = match.copy()
    for key in copy_match:
        if key in constants.FaceitIndex:
            match[constants.FaceitIndex[key]] = match[key]
            del match[key]
    return match

# Filtr matches by maps
def filterMatchesByMap(matches: list, map_name: str) -> list:
    return [match for match in matches if match['Map'] == map_name]

# Simple averaging function
def average(array: list) -> list:
    return round(sum(array) / len(array), 2) if len(array) > 0 else 0

# Returns list or object of players
def getPlayersFromMatch(match: object, merge=False) -> list:
    data = {}
    players = []
    for faction in match['teams']:
        if merge:
            players.extend([player['id'] for player in match['teams'][faction]['roster']])
        else:
            data[faction] = [player['id'] for player in match['teams'][faction]['roster']]
    if merge:
        return players
    else:
        return data

# Get average stats of matches
def getAverageOfMatches(matches: list) -> object:
    match_average = {}
    for key in constants.AVERAGE_ALLOWED:
        match_average[key] = average([float(match[key]) for match in matches])
    return match_average 

# Compare taems and give prediction ("faction1", "faction2" or "tie")
def predict(data: object, MAP:str) -> str: 
    faction1_points = faction2_points = 0
    for key in constants.AVERAGE_ALLOWED:
        if (data['faction1'][MAP][key] > data['faction2'][MAP][key]):
            faction1_points+=1
        elif (data['faction1'][MAP][key] < data['faction2'][MAP][key]):
            faction2_points+=1
        else:
            faction1_points+=1
            faction2_points+=1
    
    if faction1_points > faction2_points:
        return "faction1"
    elif faction2_points > faction1_points:
        return "faction2"
    else:
        return "tie"

# Returns the integer difference of final match score; requires 'score' key
def getScoreDifference(match: object) -> int:
    score = [int(score.strip()) for score in match['score'].split('/')]
    return abs(score[0] - score[1])