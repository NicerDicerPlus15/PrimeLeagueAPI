# Custom API für die League of Legends Prime League (WIP)

Das Programm gibt nach Eingabe der PrimeLeague-Game/Team-URL die Namen und op.gg Website der Spieler aus.

## How-To

In `example.py` wird unter `gameURL` die URL des PrimeLeague Matches eingegeben und unter `teamURL` die URL des Teams.

## Funktionen

|                    |                                                                   |
|--------------------|-------------------------------------------------------------------|
| `getNames()`       |  Gibt die Namen der Mitspieler des Matches zurück                 |
| `getOPGG()`        |  Erstellt den op.gg Link für beide Teams                          |
| `getEnemyOPGG()`   |  Erstellt den op.gg Link nur für das Gegnerteam                   |
| `getTeamName()`    |  Gibt den Namen des Teams zurück                                  |
| `getPlayerNames()` |  Gibt die Names der bestätigten Spieler eines Teams zurück        |
| `getAllOPGG()`     |  Erstellt den op.gg Link für alle bestätigten Spieler eines Teams |
| `getTeamData()`     |  Gibt die MatchID, die Goldverteilung und den Gewinner eines Prime Matches aus |


Besitzt noch mehr Funktionen, allerdings schreibt sich die README nicht von alleine.