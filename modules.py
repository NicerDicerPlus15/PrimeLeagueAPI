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

    handle1 = pl.GameSite(gameURL)
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
        gold = getTeamGold(gameData)
        
        data.append({
            "game": i,
            "gameId": game,
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

    return data