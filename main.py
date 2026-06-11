from flask import Flask, request
from datetime import datetime
import pytz
import requests

app = Flask(__name__)

POLYGON_KEY = "9MFlcEDobsWitkYr4FlO8n3ekO7QMs7P"
SWISS_TZ = pytz.timezone('Europe/Zurich')

def is_premarket():
    now = datetime.now(SWISS_TZ)
    if now.weekday() >= 5:
        return False
    t = now.hour * 60 + now.minute
    return 360 <= t < 929

def get_yahoo_price():
    r = requests.get(
        'https://query1.finance.yahoo.com/v8/finance/chart/MSTR',
        headers={'User-Agent': 'Mozilla/5.0'}
    )
    meta = r.json()['chart']['result'][0]['meta']
    price = meta.get('regularMarketPrice', 0)
    prev  = meta.get('chartPreviousClose', price)
    return price, prev

def get_polygon_price():
    r = requests.get(
        f'https://api.polygon.io/v2/last/trade/MSTR?apiKey={POLYGON_KEY}'
    )
    data = r.json()
    price = float(data['results']['p'])
    # Vortag via Yahoo
    _, prev = get_yahoo_price()
    return price, prev

@app.route('/')
def index():
    field  = request.args.get('f', 'price')
    anzahl = float(request.args.get('a', 0))
    avg    = float(request.args.get('avg', 0))
    try:
        if is_premarket():
            price, prev = get_polygon_price()
            source = 'POLYGON'
        else:
            price, prev = get_yahoo_price()
            source = 'YAHOO'

        change     = price - prev
        pct        = (change / prev) * 100
        profit_usd = (price - avg) * anzahl
        profit_pct = ((price - avg) / avg * 100) if avg > 0 else 0
        wert       = price * anzahl

        if field == 'debug':     return f"source={source} price={price} prev={prev}"
        if field == 'price':     return f"{price:.2f}"
        if field == 'pct':       return f"{'+' if pct>=0 else ''}{pct:.2f}%"
        if field == 'change':    return f"{'+' if change>=0 else ''}{change:.2f}"
        if field == 'wert':      return f"{wert:.2f}"
        if field == 'profit':    return f"{'+' if profit_usd>=0 else ''}{profit_usd:.2f}"
        if field == 'profitpct': return f"{'+' if profit_pct>=0 else ''}{profit_pct:.2f}%"
        if field == 'state':     return 'PRE' if is_premarket() else 'REGULAR'
        return f"{price:.2f}"
    except Exception as e:
        try:
            price, prev = get_yahoo_price()
            return f"{price:.2f}"
        except:
            return "—"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
