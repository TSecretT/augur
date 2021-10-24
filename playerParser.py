from faceit import Faceit
import utils
import csv
import constants

faceit = Faceit()

def saveCSV(data):
    with open('players.csv', 'a', newline='')  as output_file:
        dict_writer = csv.DictWriter(output_file, data[0].keys(), extrasaction='ignore')
        dict_writer.writeheader()
        dict_writer.writerows(data)

def main():
    for i in range(0, 100):
        matches = faceit.getMatches(page=i, past=True)

        players = []
        playersData = []

        for match in matches:
            for faction in match['teams']:
                for player in match['teams'][faction]['roster']:
                    players.append(player['nickname'])

        for j, nickname in enumerate(players):

            print(f"[Page {i}] Player {j}/{len(players)} - {nickname}", end='\r')
            info = faceit.getPlayerInfo(nickname)
            stats = faceit.getPlayerStats(info['payload']['guid'])


            whitelist = [ "m1", "m2", "k8", "k5", "k6", "s1" ]
            mapsWhitelist = [ "m1", "m2", "k1", "k2", "k3", "k4", "k5", "k6", "k7", "k8", "k9", "k10", "k11", "k12" ]

            playerData = {
                "nickname": nickname,
                "id": info['payload']['guid'],
                "level": info['payload']['games']['csgo']['skill_level'],
                "elo": info['payload']['games']['csgo']['faceit_elo']
            }

            lifeStats = utils.stripManually(stats['lifetime'], whitelist)

            for key in lifeStats:
                playerData["player_" + key] = float(lifeStats[key])
            
            segment = None

            for segment in stats['segments']:
                if segment['_id']['segmentId'] == 'csgo_map' and segment['_id']['gameMode'] == "5v5":
                    segments = segment['segments']
                    break
            
            if not segment: continue  

            playermaps = [mapname for mapname in segments]
            playermaps = "".join(playermaps)
            if "workshop" in playermaps: continue
            # print(playermaps, constants.maps)
            # if len(playermaps) < len(constants.maps): continue

            for mapname in segments:
                if mapname in ['de_cbble', 'de_ancient']: continue
                for key in utils.stripManually(segments[mapname], mapsWhitelist):
                    playerData[mapname + "_" + key] = float(segments[mapname][key])
            
            playersData.append(playerData)

        if len(playersData): saveCSV(playersData)


main()