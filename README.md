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

## KWGT Formel

$wg("mstr-api.onrender.com/?f=price", txt)$

## Stack

- Python / Flask
- Deployed auf Render.com (kostenlos)
- Daten von Yahoo Finance

## Hinweis

Render.com schläft nach 15 Minuten Inaktivität ein.
Erster Aufruf kann 30-60 Sekunden dauern bis der Server aufwacht.
Danach läuft er normal schnell.
