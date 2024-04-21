import json
import requests
from bs4 import BeautifulSoup

class PrimeGame:
    def __init__(self, game_url):
        url = "https://www.primeleague.gg/ajax/leagues_match"
        
        id = game_url[43:50]

        payload = {
            "id": id,
            "action": "init",
            "devmode": "1",
            "language": "de"
        }

        self.response = requests.post(url, data=payload)

        if self.response.status_code == 200:
            self.response_data = self.response.json()
        
        else:
            exit(f"Request failed with status code: {self.response.status_code}")
        
        
    def getNames(self):
        team1 = []
        team2 = []

        for i in range(5):
            team1.append(self.response_data['lineups']["1"][i]["gameaccounts"][0])
            team2.append(self.response_data['lineups']["2"][i]["gameaccounts"][0])

        return [team1,team2]
    
    
    def getOPGG(self):
        [team1,team2] = self.getNames()
        
        team1 = [i.replace(" ", "%20") for i in team1]
        team2 = [i.replace(" ", "%20") for i in team2]
        
        team1 = [i.replace("#", "%23") for i in team1]
        team2 = [i.replace("#", "%23") for i in team2]
    
        opurls = []

        for team in [team1,team2]:
            url = "https://www.op.gg/multisearch/euw?summoners="
            for i in range(len(team)):
                url = url + str(team[i]+",")

            url = url[:-1]
            opurls.append(url)
            
        return opurls
    
    def getEnemyOPGG(self):
        with open("options.json", "r") as fid:
            options = json.load(fid)
            
        mateName = options.get("mateName", "")
             
        [team1,team2] = self.getNames()
        
        if mateName in team1:
            team = team2
        else:
            team = team1
            
        team = [i.replace(" ", "%20") for i in team]
        team = [i.replace("#", "%23") for i in team]
            
        url = "https://www.op.gg/multisearch/euw?summoners="
        for i in range(len(team)):
            url = url + str(team[i]+",")
            
        url = url[:-1] 
        return url
    
    def getStartTime(self):
        return self.response_data["hosting_time_start"]
    
    def getScore(self):
        data = [self.response_data["score_1"], self.response_data["score_2"]]
        return data
    
    

class GameSite:
    def __init__(self, gameURL):
        response = requests.get(gameURL)
        self.soup = BeautifulSoup(response.text, 'html.parser')

    def getTeamNames(self):

        title = self.soup.find('title').text
        teams = title.split(" vs. ")
        team1 = teams[0].split(": ")[1]
        team2 = teams[1].split(" |")[0]

        return [team1, team2]
    

class PrimeTeam:
    def __init__(self, teamURL):
        response = requests.get(teamURL)
        self.soup = BeautifulSoup(response.text, 'html.parser')
    
    def getTeamName(self):
        self.teamName = self.soup.find('div', class_='page-title').find('h1').text
        return self.teamName
        
    def getPlayerNames(self):
        self.playerNames = []
        for i in self.soup.find_all('div', class_='txt-info'):
            playerNamesTemp = i.find('span', title='League of Legends » LoL Summoner Name (EU West)')
            confirmation = i.find('span', class_="txt-status-positive")
            if playerNamesTemp != None and confirmation != None:
                self.playerNames.append(playerNamesTemp.text)
        return self.playerNames
    
    def getAllOPGG(self):
        playerNames = self.getPlayerNames()
        
        playerNames = [i.replace(" ", "%20") for i in playerNames]
        playerNames = [i.replace("#", "%23") for i in playerNames]
        
        url = "https://www.op.gg/multisearch/euw?summoners="
        for i in range(len(playerNames)):
            url = url + str(playerNames[i]+",")
            
        url = url[:-1] 
        return url
    
    def getAllGames(self):
        matches = []

        matchTemp = self.soup.find_all('a', class_='table-cell-container')

        for match in matchTemp:
            if match['href'] not in matches:
                matches.append(match['href'])

        return matches
    
class RiotAPI:
    def __init__(self):
        with open("options.json", "r") as fid:
            options = json.load(fid)
        self.API_KEY = options.get("RiotAPI_Key")
        self.region = options.get("region")

    def getSummonerName(self, puuid):
        params = {
            'api_key': self.API_KEY
            }

        request_api=f"https://{self.region}.api.riotgames.com/riot/account/v1/accounts/by-puuid/{puuid}"

        try:
            response = requests.get(request_api, params=params)
            summonerName = response.json()
        except requests.exceptions.RequestException as e:
            print(f'Issues getting Riot API data: {e}')

        return summonerName["gameName"]

    def getGames(self, startTime, nrGames):
        with open("options.json", "r") as fid:
            options = json.load(fid)

        puuid = options.get("puuid")[0]

        params = {
            'api_key': self.API_KEY,
            'count': nrGames,
            'startTime': startTime - 2 * 3600,
            'endTime': startTime + 2 * 3600,
            'queue': 0
            }
        
        request_api=f"https://{self.region}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids"

        try:
            response = requests.get(request_api, params=params)
            matchids = response.json()
        except requests.exceptions.RequestException as e:
            print(f'Issues getting Riot API data: {e}')
        
        return matchids


    def getGameData(self,matchid):
        params = {
            'api_key': self.API_KEY
            }
        
        request_api=f'https://{self.region}.api.riotgames.com/lol/match/v5/matches/{matchid}'

        try:
            response = requests.get(request_api, params=params)
            matchData = response.json()
        except requests.exceptions.RequestException as e:
            print(f'Issues getting Riot API data: {e}')

        return matchData
    
    def getParticipants(self, matchData):
        participants = matchData["metadata"]["participants"]
        return participants
    
    def getTimeline(self, matchid):
        params = {
            'api_key': self.API_KEY
            }
        
        request_api=f'https://{self.region}.api.riotgames.com/lol/match/v5/matches/{matchid}/timeline'

        try:
            response = requests.get(request_api, params=params)
            timeline = response.json()
        except requests.exceptions.RequestException as e:
            print(f'Issues getting Riot API data: {e}')

        return timeline

