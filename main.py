from flask import Flask, request
from datetime import datetime
import pytz
import requests

app = Flask(__name__)

ALPHA_KEY = "DU2HMH0YWV62D3QP"
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

def get_alpha_price():
    r = requests.get(
        f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=MSTR&apikey={ALPHA_KEY}'
    )
    data = r.json().get('Global Quote', {})
    regular   = float(data.get('05. price', 0))
    premarket = float(data.get('08. previous close', 0))
    if regular == 0 or premarket == 0:
        return get_yahoo_price()
    return premarket, regular

@app.route('/')
def index():
    field  = request.args.get('f', 'price')
    anzahl = float(request.args.get('a', 0))
    avg    = float(request.args.get('avg', 0))
    try:
        if is_premarket():
            price, prev = get_alpha_price()
            source = 'ALPHA'
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
        if field
