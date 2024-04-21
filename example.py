import PrimeLeagueAPI as pl
import modules as md

if __name__ == "__main__":
    gameURL = "https://www.primeleague.gg/leagues/matches/1104947-ebw-unleashed-vs-back-to-circus"
    teamURL = "https://www.primeleague.gg/leagues/teams/181171-back-to-circus"
    
    handle1 = pl.PrimeGame(gameURL)
    handle2 = pl.PrimeTeam(teamURL)
    handle3 = pl.RiotAPI()
    
    names = handle1.getNames()
    op_urls = handle1.getOPGG()
    teamName = handle2.getTeamName()
    playerNames = handle2.getPlayerNames()
    playerOPgg = handle2.getAllOPGG()

    gameData = md.getTeamData(gameURL)
    
    print("Player Names:")
    [print(name) for name in names]
    print()
    print("Player op.gg:")
    [print(urls) for urls in op_urls]
    print()
    print(f'Team "{teamName}" Player Names:')
    print(playerNames)
    print()
    print("Team Player op.gg:")
    print(playerOPgg)
    print()
    print("Prime Game Data")
    print(gameData)
    