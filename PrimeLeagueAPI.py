import json
import requests

def prime(game_url):
    url = "https://www.primeleague.gg/ajax/leagues_match"
    
    with open("options.json", "r") as file:
        options = json.load(file)
        
    mateName = options.get("mateName", "")

    id = game_url[43:50]

    payload = {
        "id": id,
        "action": "init",
        "devmode": "1",
        "language": "de"
    }

    # Send the POST request with the provided data, headers, and cookies
    response = requests.post(url, data=payload)

    # Check if the request was successful and handle the response data
    if response.status_code == 200:
        response_data = response.json()

        team1 = []
        team2 = []

        url = "https://www.op.gg/multisearch/euw?summoners="

        for i in range(5):
            team1.append(response_data['lineups']["1"][i]["gameaccounts"][0])
            team2.append(response_data['lineups']["2"][i]["gameaccounts"][0])
            
        print(team1)
        print(team2)

        team1 = [i.replace(" ", "%20") for i in team1]
        team2 = [i.replace(" ", "%20") for i in team2]
        
        team1 = [i.replace("#", "%23") for i in team1]
        team2 = [i.replace("#", "%23") for i in team2]

        if mateName in team1:
            team = team2

        else:
            team = team1

        for i in range(len(team)):
            url = url + str(team[i]+",")

        url = url[:-1]
        # print(url)
        return url
    else:
        print(f"Request failed with status code: {response.status_code}")


if __name__ == "__main__":
    gameURL = ""
    opgg = prime(gameURL)
    print(opgg)