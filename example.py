import PrimeLeagueAPI as pl

if __name__ == "__main__":
    gameURL = ""
    teamURL = ""
    
    handle1 = pl.PrimeGame(gameURL)
    handle2 = pl.PrimeTeam(teamURL)
    
    names = handle1.getNames()
    op_urls = handle1.getOPGG()
    teamName = handle2.getTeamName()
    playerNames = handle2.getPlayerNames()
    playerOPgg = handle2.getAllOPGG()
    
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
    