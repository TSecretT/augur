MATCHMAKING_STATES = [
    "SUBSTITUTION",
    "CAPTAIN_PICK",
    "VOTING",
    "CONFIGURING",
    "READY",
    "ONGOING",
    "MANUAL_RESULT",
    "PAUSED",
    "ABORTED"
]

maps = [
    'de_cache',
    'de_dust2',
    'de_mirage',
    'de_nuke',
    'de_overpass',
    'de_inferno',
    'de_vertigo',
    'de_train',
    'de_ancient'
]

FaceitIndex = {
   "c2":"K/D Ratio",
   "c3":"K/R Ratio",
   "c4":"Headshots %",
   "c5":"Final Score",
   "c6":"Team K/D Ratio",
   "c7":"Team K/R Ratio",
   "c8":"Team Headshots %",
   "c9":"Team Headshots",
   "elo":"Elo",
   "i0":"Region",
   "i1":"Map",
   "i10":"Result",
   "i12":"Rounds",
   "i13":"Headshots",
   "i14":"Triple Kills",
   "i15":"Quadro Kills",
   "i16":"Penta Kills",
   "i17":"Team Win",
   "i18":"Score",
   "i19":"Overtime score",
   "i2":"Winner",
   "i3":"First Half Score",
   "i4":"Second Half Score",
   "i5":"Team",
   "i6":"Kills",
   "i7":"Assists",
   "i8":"Deaths",
   "i9":"MVPs",
   "k1":"Average Kills",
   "k10":"Average Triple Kills",
   "k11":"Average Quadro Kills",
   "k12":"Average Penta Kills",
   "k13":"Team Average K/D Ratio",
   "k14":"Team Average K/R Ratio",
   "k15":"Team Average Headshots %",
   "k16":"Team Headshots per Match",
   "k2":"Average Deaths",
   "k3":"Average Assists",
   "k4":"Average MVPs",
   "k5":"Average K/D Ratio",
   "k6":"Win Rate %",
   "k7":"Headshots per Match",
   "k8":"Average Headshots %",
   "k9":"Average K/R Ratio",
   "m1":"Matches",
   "m10":"Triple Kills",
   "m11":"Quadro Kills",
   "m12":"Penta Kills",
   "m13":"Total Headshots %",
   "m14":"K/R Ratio",
   "m15":"Total K/D Ratio",
   "m16":"Total K/R Ratio",
   "m17":"Total Headshots %",
   "m18":"Total Headshots per Match",
   "m2":"Wins",
   "m3":"Kills",
   "m4":"Deaths",
   "m5":"Assists",
   "m6":"MVPs",
   "m7":"K/D Ratio",
   "m8":"Rounds",
   "m9":"Headshots",
   "s0":"Recent Results",
   "s1":"Current Win Streak",
   "s2":"Longest Win Streak"
}

AVERAGE_ALLOWED = [
    "Kills", "Deaths", "Assists", "HS %", "K/D", "K/R", "elo", 
]

LOWERCASE_OF_KEY = {
    "Kills": "kills",
    "Deaths": "deaths",
    "Assists": "assists",
    "HS %": "hs",
    "K/D": "kd",
    "K/R": "kr",
    "elo": "elo"
}

KEYS_TO_KEEP = [
    "id", "state", "status", "teams", "voting", "results", "createdAt", "finishedAt",
    "prediction", "data", "parsing_time", "score", "prediction_correct", "checking_time"
]

DEFAULT_FROM = "1970-01-01T01:00:00+0000"
DEFAULT_TO = "2020-12-11T21:20:28+0000"
TIE_SCORE_DIFFERENCE = 4