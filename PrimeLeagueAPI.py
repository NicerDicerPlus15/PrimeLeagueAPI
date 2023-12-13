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

        response = requests.post(url, data=payload)

        if response.status_code == 200:
            self.response_data = response.json()
        
        else:
            exit(f"Request failed with status code: {response.status_code}")
        
        
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