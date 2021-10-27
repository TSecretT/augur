from faceit import Faceit
import utils
import csv
import constants

faceit = Faceit()

def saveCSV(data):
    with open('players.csv', 'a', newline='', encoding='utf-8')  as output_file:
        dict_writer = csv.DictWriter(output_file, data[0].keys(), extrasaction='ignore')
        # dict_writer.writeheader()
        dict_writer.writerows(data)

def main():
    for i in range(0, 10):
        matches = faceit.getMatches(page=i, past=True)

        players = []
        playersData = []

        for match in matches:
            for faction in match['teams']:
                for player in match['teams'][faction]['roster']:
                    players.append(player['nickname'])

        for j, nickname in enumerate(players):

            print(f"[Page {i}] Player {j}/{len(players)} - {nickname}", end='\n\r')

            try:
                info = faceit.getPlayerInfo(nickname)
                stats = faceit.getPlayerStats(info['payload']['guid'])
            except:
                continue

            whitelist = [ "m1", "m2", "k8", "k5", "k6", "s1" ]
            mapsWhitelist = [ "m1", "m2", "k1", "k2", "k3", "k4", "k5", "k6", "k7", "k8", "k9", "k10", "k11", "k12" ]

            playerData = {
                "nickname": nickname,
                "id": info['payload']['guid'],
                "level": info['payload']['games']['csgo']['skill_level'],
                "elo": info['payload']['games']['csgo']['faceit_elo']
            }

            try:
                lifeStats = utils.stripManually(stats['lifetime'], whitelist)
            except:
                continue

            for key in lifeStats:
                playerData["player_" + key] = float(lifeStats[key])
            
            segment = None

            for segment_ in stats['segments']:
                if segment_['_id']['segmentId'] == 'csgo_map' and segment_['_id']['gameMode'] == "5v5":
                    segment = segment_['segments']
                    break
            
            if not segment: continue  

            playermaps = [mapname for mapname in segment]
            playermapsString = "".join(playermaps)

            if "workshop" in playermapsString: continue

            # case 1:
            # players -> ['de_mirage', 'de_inferno', 'de_nuke', 'de_train']
            # constants -> ['de_mirage', 'de_inferno', 'de_nuke']
            if len(playermaps) > len(constants.maps):
                playermaps = [x for x in playermaps if x in constants.maps]

        
            # case 2:
            # players -> ['de_mirage', 'de_inferno']
            # constants -> ['de_mirage', 'de_inferno', 'de_nuke']
            if len(playermaps) < len(constants.maps): continue

            # case 3:
            # players -> ['de_mirage', 'de_inferno', 'de_ancient']
            # constants -> ['de_mirage', 'de_inferno', 'de_nuke']
            if (len(playermaps) == len(constants.maps)) and (playermaps.sort() != constants.maps.sort()): continue


            added_maps = []
            for mapname in playermaps:
                added_maps.append(mapname)
                for key in utils.stripManually(segment[mapname], mapsWhitelist):
                    playerData[mapname + "_" + key] = float(segment[mapname][key])

            playersData.append(playerData)

        if len(playersData): saveCSV(playersData)

main()