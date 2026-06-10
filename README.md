# MSTR Widget API 🟠

Eine einfache API die live MSTR (MicroStrategy) Aktienkursdaten liefert.
Gebaut für die Nutzung mit KWGT Widget Maker auf Android.

## Live API
https://mstr-api.onrender.com

## Endpunkte

| Parameter | Beschreibung | Beispiel |
|-----------|-------------|---------|
| `f=price` | Aktueller Kurs in USD | `/?f=price` |
| `f=pct` | Tagesveränderung in % | `/?f=pct` |
| `f=change` | Tagesveränderung in USD | `/?f=change` |
| `f=wert` | Portfoliowert | `/?f=wert&a=10&avg=300` |
| `f=profit` | Gewinn/Verlust in USD | `/?f=profit&a=10&avg=300` |
| `f=profitpct` | Gewinn/Verlust in % | `/?f=profitpct&a=10&avg=300` |

## Parameter

- `a` = Anzahl Aktien
- `avg` = Durchschnittlicher Einstandskurs in USD

## Beispiel

https://mstr-api.onrender.com/?f=profitpct&a=10&avg=300

## Stack

- Python / Flask
- Deployed auf Render.com (kostenlos)
- Daten von Yahoo Finance

## KWGT Formeln

### Kurs & Tagesveränderung
Preis:
$wg("mstr-api.onrender.com/?f=price", txt)$

Tagesveränderung %:
$wg("mstr-api.onrender.com/?f=pct", txt)$

Tagesveränderung USD:
$wg("mstr-api.onrender.com/?f=change", txt)$

### Portfolio (a=Anzahl, avg=Einstand)
Portfoliowert:
$wg("mstr-api.onrender.com/?f=wert&a=10&avg=300", txt)$

Gewinn/Verlust USD:
$wg("mstr-api.onrender.com/?f=profit&a=10&avg=300", txt)$

Gewinn/Verlust %:
$wg("mstr-api.onrender.com/?f=profitpct&a=10&avg=300", txt)$

## KWGT Einstellungen
- Hintergrundfarbe: #0a0b0f
- Eckenradius: 20
- Titelfarbe MSTR: #f7931a
- Preisfarbe: #ffffff
- Änderung positiv: #00e676
- Änderung negativ: #ff4444
- Preisgrösse: 42
- Titelgrösse: 14
- Änderungsgrösse: 14

## Hinweis
10 und 300 in den Portfolio-Formeln mit
eigenen Werten ersetzen!
Render.com schläft nach 15 Minuten Inaktivität ein.
Erster Aufruf kann 30-60 Sekunden dauern bis der Server aufwacht.
Danach läuft er normal schnell.
