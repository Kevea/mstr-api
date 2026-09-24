from flask import Flask, request
from datetime import datetime
import pytz
import requests

app = Flask(__name__)

SWISS_TZ = pytz.timezone('Europe/Zurich')

# Yahoo blockt Anfragen ohne Browser-Kennung
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

SYMBOLS = {
    'MSTR':   'MSTR',
    'PLTR':   'PLTR',
    'SPACEX': 'SPCX',      # Space Exploration Technologies Corp., NasdaqGS
    'WORLD':  'SWDA.SW',   # iShares Core MSCI World UCITS ETF USD (Acc)
    'EUROPE': 'IMAE.AS',   # iShares Core MSCI Europe UCITS ETF EUR (Acc)
}


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


def get_price(symbol):
    url = f'https://query2.finance.yahoo.com/v8/finance/chart/{symbol}?interval=1d&range=7d'
    r = requests.get(url, headers=HEADERS, timeout=10)
    result = r.json()['chart']['result'][0]
    meta = result['meta']
    price = float(meta['regularMarketPrice'])

    # meta.chartPreviousClose ist NICHT der Vortagesschluss, sondern der Schluss vor
    # dem angefragten Zeitraum. Der Vortagesschluss ist der vorletzte Balken — aber nur,
    # wenn der letzte Balken zum laufenden Handelstag gehoert (sonst waere es ein Tag zu weit).
    rows = [(t, c) for t, c in zip(result['timestamp'], result['indicators']['quote'][0]['close']) if c is not None]
    offset = meta.get('gmtoffset', 0)
    day = lambda epoch: (int(epoch) + offset) // 86400
    if len(rows) >= 2 and day(rows[-1][0]) == day(meta['regularMarketTime']):
        prev = rows[-2][1]
    else:
        prev = rows[-1][1]

    return price, float(prev), meta.get('currency', '')


def fx_rate(frm, to):
    if not to or frm == to:
        return 1.0
    rate, _, _ = get_price(f'{frm}{to}=X')
    return rate


@app.route('/')
def index():
    field = request.args.get('f', 'price')
    key = request.args.get('s', 'MSTR').upper()
    symbol = SYMBOLS.get(key, key)
    target_cur = request.args.get('cur', '').upper()

    try:
        anzahl = float(request.args.get('a', 0))
        avg = float(request.args.get('avg', 0))

        price, prev, cur = get_price(symbol)
        rate = fx_rate(cur, target_cur)
        price *= rate
        prev *= rate

        change = price - prev
        pct = (change / prev) * 100 if prev else 0
        profit_usd = (price - avg) * anzahl
        profit_pct = ((price - avg) / avg * 100) if avg > 0 else 0
        wert = price * anzahl
        state = market_state()

        if field == 'debug':     return f'{symbol} state={state} price={price:.4f} prev={prev:.4f} cur={target_cur or cur}'
        if field == 'price':     return f'{price:.2f}'
        if field == 'pct':       return f"{'+' if pct>=0 else ''}{pct:.2f}%"
        if field == 'change':    return f"{'+' if change>=0 else ''}{change:.2f}"
        if field == 'wert':      return f'{wert:.2f}'
        if field == 'profit':    return f"{'+' if profit_usd>=0 else ''}{profit_usd:.2f}"
        if field == 'profitpct': return f"{'+' if profit_pct>=0 else ''}{profit_pct:.2f}%"
        if field == 'cur':       return target_cur or cur
        if field == 'state':     return state
        return f'{price:.2f}'
    except Exception:
        return '—'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
