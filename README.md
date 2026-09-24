# Aktien-Widget API 📈

Live-Kurse für KWGT-Widgets auf Android.
Datenquelle: Yahoo Finance (kein API-Key nötig, deckt US-Titel **und** europäische UCITS-ETFs ab).

## Live API
https://mstr-api.onrender.com

## Symbole

Mit `s=` wird das Wertpapier gewählt. Ohne Angabe: MSTR (damit bestehende Widgets weiterlaufen).

| `s=` | Wertpapier | Ticker | Währung |
|------|-----------|--------|---------|
| `MSTR` | MicroStrategy | MSTR | USD |
| `PLTR` | Palantir | PLTR | USD |
| `SPACEX` | Space Exploration Technologies | SPCX | USD |
| `WORLD` | iShares Core MSCI World UCITS ETF (Acc) | SWDA.SW | USD |
| `EUROPE` | iShares Core MSCI Europe UCITS ETF EUR (Acc) | IMAE.AS | EUR |

Jeder andere gültige Yahoo-Ticker funktioniert ebenfalls direkt, z. B. `s=AAPL` oder `s=EUNL.DE`.

## Endpunkte

| Parameter | Beschreibung | Beispiel |
|-----------|-------------|---------|
| `f=price` | Aktueller Kurs | `/?f=price&s=PLTR` |
| `f=pricecur` | Kurs **mit Währung** | `/?f=pricecur&s=PLTR` → `191.79 USD` |
| `f=pct` | Tagesveränderung in % | `/?f=pct&s=PLTR` |
| `f=change` | Tagesveränderung absolut | `/?f=change&s=PLTR` |
| `f=wert` | Positionswert | `/?f=wert&s=PLTR&a=10` |
| `f=profit` | Gewinn/Verlust absolut | `/?f=profit&s=PLTR&a=10&avg=150` |
| `f=profitpct` | Gewinn/Verlust in % | `/?f=profitpct&s=PLTR&a=10&avg=150` |
| `f=cur` | Währung des Kurses | `/?f=cur&s=EUROPE` |
| `f=state` | Marktphase (US-Zeiten) | `/?f=state` |
| `f=debug` | Alle Werte auf einmal | `/?f=debug&s=WORLD` |
| `f=list` | **Eine Spalte für mehrere Positionen** | `/?f=list&col=pricecur&p=…` |
| `f=table` | **Ganze Tabelle in einem Wert** | `/?f=table&p=…` |

## Parameter

- `s` = Wertpapier (siehe Tabelle), Standard `MSTR`
- `a` = Anzahl Stück
- `avg` = Durchschnittlicher Einstandskurs
- `cur` = Zielwährung, rechnet den Kurs um (z. B. `cur=CHF`)
- `p` = Mehrere Positionen für `f=list` / `f=table` (siehe unten)
- `col` = Welche Spalte `f=list` ausgibt, Standard `pricecur`
- `cols` = Welche Spalten `f=table` ausgibt, Standard `name,pricecur,profitpct`

`avg` muss in derselben Währung wie der ausgegebene Kurs angegeben werden —
bei `cur=CHF` also der Einstandskurs in CHF.

## Mehrere Positionen auf einmal

Statt pro Wert eine eigene Anfrage zu stellen, holt `f=list` bzw. `f=table`
**alle Positionen in einer einzigen Anfrage**. Das Depot steht im Parameter `p`:

```
p=SYMBOL:ANZAHL:EINSTAND[:WÄHRUNG],SYMBOL:ANZAHL:EINSTAND[:WÄHRUNG],…
```

Beispiel (Beispielzahlen, kein echtes Depot):

```
/?f=table&p=MSTR:2:100,PLTR:5:150,EUROPE:3:90:CHF
```

```
MSTR    162.20 USD  +62.20%
PLTR    191.79 USD  +27.86%
EUROPE   97.73 CHF   +8.59%
```

**`f=table`** padded die Spalten mit Leerzeichen — das steht nur dann bündig
untereinander, wenn das Textfeld eine **Monospace-Schrift** benutzt.

**`f=list`** liefert nur eine Spalte, eine Zeile pro Position. Drei solcher
Felder nebeneinander ergeben saubere Spalten **unabhängig von der Schriftart** —
der empfohlene Weg, wenn keine Monospace-Schrift zur Verfügung steht:

```
$wg("mstr-api.onrender.com/?f=list&col=name&p=…", txt)$
$wg("mstr-api.onrender.com/?f=list&col=pricecur&p=…", txt)$
$wg("mstr-api.onrender.com/?f=list&col=profitpct&p=…", txt)$
```

Als `col` bzw. in `cols` sind alle Feldnamen aus der Endpunkt-Tabelle erlaubt
(`name`, `price`, `pricecur`, `pct`, `change`, `wert`, `profit`, `profitpct`, `cur`).
Ein Symbol, das sich nicht abrufen lässt, erscheint als `—`, ohne die übrigen
Zeilen zu verlieren.

Kursdaten werden 60 Sekunden zwischengespeichert, damit mehrere Spalten-Felder
nicht jedes Mal dieselben Abfragen bei Yahoo auslösen.

## KWGT Formeln

```
Kurs:              $wg("mstr-api.onrender.com/?f=price&s=PLTR", txt)$
Kurs mit Währung:  $wg("mstr-api.onrender.com/?f=pricecur&s=PLTR", txt)$
Tagesveränderung:  $wg("mstr-api.onrender.com/?f=pct&s=PLTR", txt)$
Gewinn/Verlust %:  $wg("mstr-api.onrender.com/?f=profitpct&s=PLTR&a=10&avg=150", txt)$
ETF in CHF:        $wg("mstr-api.onrender.com/?f=price&s=EUROPE&cur=CHF", txt)$
```

## Fertige Formelsammlung

`KWGT-Formeln-Beispiel.pdf` im Repo enthält alle Formeln zum Kopieren —
Einzelwerte pro Position, die drei Spalten-Felder und die Ein-Feld-Tabelle.
Die dort eingetragenen Stückzahlen und Einstandskurse sind Beispielwerte,
einfach durch die eigenen ersetzen.

## KWGT Design
- Hintergrundfarbe: #0a0b0f
- Eckenradius: 20
- Titelfarbe MSTR: #f7931a
- Preisfarbe: #ffffff
- Preisgrösse: 42
- Titelgrösse: 14

## Stack
- Python / Flask
- Yahoo Finance Chart-API (v8, ohne Key)
- Deployed auf Render.com (kostenlos)

## Hinweise
- Render schläft nach 15 Min Inaktivität ein. Erster Aufruf kann 30–60 Sek dauern.
- Yahoo blockt Anfragen ohne Browser-User-Agent — der Header ist im Code gesetzt.
- Der Vortagesschluss wird aus der Kursreihe abgeleitet, **nicht** aus
  `meta.chartPreviousClose`: dieses Feld liefert den Schluss *vor dem angefragten
  Zeitraum*, was je nach `range` mehrere Tage danebenliegt.
- Yahoos v7-Quote-Endpunkt (`/v7/finance/quote`) antwortet nur noch mit
  `Unauthorized` und ist als Fallback unbrauchbar.
- Pre-Market-Kurse liefert die kostenlose API nicht.
