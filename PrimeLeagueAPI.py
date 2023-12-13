import json
import requests

class PrimeLeagueAPI:
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
        
        # with open("options.json", "r") as file:
        #     options = json.load(file)
        
        # mateName = options.get("mateName", "")
        
        # if mateName in team1:
        #     team = team2
        # else:
        #     team = team1
        
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
