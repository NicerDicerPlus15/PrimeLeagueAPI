# Custom API für die League of Legends Prime League (WIP)

Das Programm gibt nach Eingabe der PrimeLeague-Game-URL die op.gg Seider der Gegner aus.

## How-To

Die `option.json` Datei benötigt den Username eines Spielers im Team im Format `Username%23Hash`.

Das Hashtag wird durch ein `%23` ersetzt.

Zum Beispiel: `HideOnBush%23EUW` für `HideOnBush#EUW`.

In `PrimeLeagueAPI.py` wird unter `gameURL` die URL des PrimeLeague Matches eingegeben.