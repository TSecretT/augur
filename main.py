from faceit import Faceit
import utils
import constants


faceit = Faceit()


def main():

    for i in range(0, 10):
        matches = faceit.getMatches(page=i, past=True)
        
        for match in matches:
            players = utils.getPlayersFromMatch(match)
            teamStats = {}
            for team in players:
                for playerID in players[team]:
                    teamStats[playerID] = []
                    playerStats = faceit.getPlayerMatchesStats(playerID)
                    for playerStat in playerStats:
                        playerStat = utils.convertMatchKeys(playerStat)
                        playerStat = utils.stripPlayerMatch(playerStat)
                        teamStats[playerID].append(playerStat)

            stats = {}

            for player in teamStats:
                playerStats = {}
                for key in constants.AVERAGE_ALLOWED:
                    playerStats[key] = []
                for match in teamStats[player]:
                    for key in match:
                        playerStats[key].append(float(match[key]))
                for key in playerStats.copy():
                    playerStats[key] = utils.average(playerStats[key])
                stats[player] = playerStats



if __name__ == "__main__":
    main()