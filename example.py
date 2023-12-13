import PrimeLeagueAPI as pl

if __name__ == "__main__":
    gameURL = ""
    
    handle = pl.PrimeLeagueAPI(gameURL)
    names = handle.getNames()
    op_urls = handle.getOPGG()
    
    [print(name) for name in names]
    [print(urls) for urls in op_urls]
    