import PrimeLeagueAPI as pl
import json

def getTeamGold(gameData):
    gold1 = 0
    gold2 = 0

    with open("options.json", "r") as fid:
            options = json.load(fid)
    
    puuid = options.get("puuid")

    myTeamId = 0

    for i in range(10):
        if gameData["info"]["participants"][i]["puuid"] in puuid:
            myTeamId = gameData["info"]["participants"][i]["teamId"]

    for i in gameData["info"]["participants"]:
        if i["teamId"] == myTeamId:
            gold1 += int(i["goldEarned"])
        else:
            gold2 += int(i["goldEarned"])

    data1 = ["myTeam", gameData["info"]["teams"][0]["win"], gold1]
    data2 = ["enemyTeam", gameData["info"]["teams"][1]["win"], gold2]

    return [data1, data2]

def getTeamData(gameURL):

    with open("options.json", "r") as fid:
            options = json.load(fid)

    myTeam = options.get("myTeamName")

    handle1 = pl.Parser(gameURL)
    handle2 = pl.PrimeGame(gameURL)
    handle3 = pl.RiotAPI()

    startTime = handle2.getStartTime()
    
    teamNames = handle1.getTeamNames()
    score = handle2.getScore()

    if teamNames[0] == myTeam:
        enemyTeam = teamNames[1]
    else:
        enemyTeam = teamNames[0]

    nrGames = score[0] + score[1]

    games = handle3.getGames(startTime, nrGames)

    data = []
    i = 1

    for game in games:
        gameData = handle3.getGameData(game)

        try:
            gold = getTeamGold(gameData)
            timestamp = gameData["info"]["gameCreation"]
            
            data.append({
                "game": i,
                "gameId": game,
                "timestamp": timestamp,
                "team1": {
                    "teamName": myTeam,
                    "win": gold[0][1],
                    "goldEarned": gold[0][2]
                    },
                "team2": {
                    "teamName": enemyTeam,
                    "win": gold[1][1],
                    "goldEarned": gold[1][2]
                    },

            })
            i = i + 1
        
        except: 
            if gameData["status"]["status_code"] != 200:
                print(f'Status Code {gameData["status"]["status_code"]}')
                data = 404

    return data