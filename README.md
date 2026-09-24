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

## Parameter

- `s` = Wertpapier (siehe Tabelle), Standard `MSTR`
- `a` = Anzahl Stück
- `avg` = Durchschnittlicher Einstandskurs
- `cur` = Zielwährung, rechnet den Kurs um (z. B. `cur=CHF`)

`avg` muss in derselben Währung wie der ausgegebene Kurs angegeben werden —
bei `cur=CHF` also der Einstandskurs in CHF.

## KWGT Formeln

```
Kurs:              $wg("mstr-api.onrender.com/?f=price&s=PLTR", txt)$
Kurs mit Währung:  $wg("mstr-api.onrender.com/?f=pricecur&s=PLTR", txt)$
Tagesveränderung:  $wg("mstr-api.onrender.com/?f=pct&s=PLTR", txt)$
Gewinn/Verlust %:  $wg("mstr-api.onrender.com/?f=profitpct&s=PLTR&a=10&avg=150", txt)$
ETF in CHF:        $wg("mstr-api.onrender.com/?f=price&s=EUROPE&cur=CHF", txt)$
```

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
