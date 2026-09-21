# motd-slumpat-latincitat

Skriver ut ett slumpmässigt latinskt citat med svensk översättning,
t.ex. som en del av en MOTD (message of the day).

Citaten kommer ursprungligen från Wikipedia-artikeln
["Latinska ordspråk och talesätt"](https://sv.wikipedia.org/wiki/Latinska_ordspråk_och_talesätt),
normaliserade till en enkel, scriptvänlig textfil.

Andra citat läggs även till denna fil utöver det som är taget från Wikipedia.

## Filer

- `latin_citat_normaliserat.txt` – ett citat per rad, formatet
  `Latinskt citat|Svensk översättning/förklaring`.
- `slumpat_citat.sh` – körbart bash/zsh-skript som skriver ut ett
  slumpat citat från textfilen.

## Användning

```sh
./slumpat_citat.sh
```
