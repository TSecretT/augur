import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from faceit import Faceit



class PlayersParse(unittest.TestCase):
    
    def setUp(self) -> None:
        self.faceit = Faceit()

    def test_getMatches(self):
        matches = self.faceit.getMatches()
        self.assertLessEqual(1, len(matches))
        self.assertIn("game", matches[0].keys())

    # def test_getLiveMatches(self):
    #     self.liveMatches = self.faceit.getLiveMatches()
    #     self.assertLessEqual(1, len(self.liveMatches))
    #     self.assertIn("status", self.liveMatches[0].keys())
    #     self.assertEqual("LIVE", self.liveMatches[0]['status'])

    def test_getMatchDetails(self):
        matches = self.faceit.getMatches()
        match = self.faceit.getMatchDetails(id=matches[0]['id'])
        self.assertIn("status", match.keys())
    
    def test_getPlayerMatchesStats(self):
        matches = self.faceit.getMatches()
        for match in matches:
            if 'teams' in match\
                and 'faction1' in match['teams']\
                    and len(match['teams']['faction1'])\
                        and "roster" in match['teams']['faction1']:
                            playerID = match['teams']['faction1']['roster'][0]['id']
                            break
        matches = self.faceit.getPlayerMatchesStats(id = playerID)
        self.assertLessEqual(1, len(matches))
        self.assertIn("matchId", matches[0]['_id'])

    def test_getPlayerStats(self):
        matches = self.faceit.getMatches()
        playerID = matches[0]['teams']['faction1']['roster'][0]['id']
        stats = self.faceit.getPlayerStats(id=playerID)
        self.assertIn("lifetime", stats)
        self.assertIn("segments", stats)

    def test_getPlayerInfo(self):
        info = self.faceit.getPlayerInfo("TSecret_")
        self.assertIn('result', info)
        self.assertEqual('ok', info['result'])

if __name__ == '__main__':
    unittest.main()