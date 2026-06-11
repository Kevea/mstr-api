from flask import Flask, request
from datetime import datetime
import pytz
import requests

app = Flask(__name__)

FINNHUB_KEY = "d8l7pehr01qut1f9kk8gd8l7pehr01qut1f9kk90"
SWISS_TZ = pytz.timezone('Europe/Zurich')

def market_state():
    now = datetime.now(SWISS_TZ)
    if now.weekday() >= 5:
        return 'CLOSED'
    t = now.hour * 60 + now.minute
    if 360 <= t < 929:
        return 'PRE'
    if 929 <= t < 1320:
        return 'OPEN'
    if 1320 <= t < 1440:
        return 'POST'
    return 'CLOSED'

def get_price():
    r = requests.get(
        f'https://finnhub.io/api/v1/quote?symbol=MSTR&token={FINNHUB_KEY}'
    )
    data = r.json()
    price = float(data['c'])
    prev  = float(data['pc'])
    return price, prev

@app.route('/')
def index():
    field  = request.args.get('f', 'price')
    anzahl = float(request.args.get('a', 0))
    avg    = float(request.args.get('avg', 0))
    try:
        price, prev = get_price()
        change     = price - prev
        pct        = (change / prev) * 100
        profit_usd = (price - avg) * anzahl
        profit_pct = ((price - avg) / avg * 100) if avg > 0 else 0
        wert       = price * anzahl
        state      = market_state()

        if field == 'debug':     return f"state={state} price={price} prev={prev}"
        if field == 'price':     return f"{price:.2f}"
        if field == 'pct':       return f"{'+' if pct>=0 else ''}{pct:.2f}%"
        if field == 'change':    return f"{'+' if change>=0 else ''}{change:.2f}"
        if field == 'wert':      return f"{wert:.2f}"
        if field == 'profit':    return f"{'+' if profit_usd>=0 else ''}{profit_usd:.2f}"
        if field == 'profitpct': return f"{'+' if profit_pct>=0 else ''}{profit_pct:.2f}%"
        if field == 'state':     return state
        return f"{price:.2f}"
    except:
        return "—"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
