# MSTR Widget API 🟠

Live MSTR (MicroStrategy) Aktienkurs API für KWGT Widget auf Android.
Datenquelle: Finnhub.io (60 Anfragen/Min, kostenlos)

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
| `f=debug` | Alle Werte anzeigen | `/?f=debug` |

## Parameter
- `a` = Anzahl Aktien
- `avg` = Durchschnittlicher Einstandskurs in USD

## KWGT Formeln
Preis:
$wg("mstr-api.onrender.com/?f=price", txt)$

Tagesveränderung %:
$wg("mstr-api.onrender.com/?f=pct", txt)$

Portfoliowert:
$wg("mstr-api.onrender.com/?f=wert&a=10&avg=300", txt)$

Gewinn/Verlust %:
$wg("mstr-api.onrender.com/?f=profitpct&a=10&avg=300", txt)$

## KWGT Design
- Hintergrundfarbe: #0a0b0f
- Eckenradius: 20
- Titelfarbe MSTR: #f7931a
- Preisfarbe: #ffffff
- Preisgrösse: 42
- Titelgrösse: 14

## Stack
- Python / Flask
- Finnhub.io API (kostenlos)
- Deployed auf Render.com (kostenlos)

## Hinweis
Render schläft nach 15 Min Inaktivität ein.
Erster Aufruf kann 30-60 Sek dauern.
Pre-Market Preise sind mit kostenlosen APIs leider nicht verfügbar.
