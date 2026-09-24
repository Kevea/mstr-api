from flask import Flask, request, Response
from datetime import datetime
import pytz
import requests
import time

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

# Eine Tabellenabfrage holt fuenf Kurse plus Wechselkurs. Ohne Cache waeren das
# bei jedem Widget-Refresh und jeder Spalte erneut so viele Anfragen an Yahoo.
CACHE_TTL = 60
_cache = {}


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


def fetch(symbol):
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


def get_price(symbol):
    hit = _cache.get(symbol)
    if hit and time.time() - hit[0] < CACHE_TTL:
        return hit[1]
    data = fetch(symbol)
    _cache[symbol] = (time.time(), data)
    return data


def fx_rate(frm, to):
    if not to or frm == to:
        return 1.0
    rate, _, _ = get_price(f'{frm}{to}=X')
    return rate


def sgn(v):
    return '+' if v >= 0 else ''


def values(key, anzahl, avg, target_cur):
    price, prev, cur = get_price(SYMBOLS.get(key, key))
    rate = fx_rate(cur, target_cur)
    price *= rate
    prev *= rate

    change = price - prev
    pct = (change / prev) * 100 if prev else 0
    profit = (price - avg) * anzahl
    profit_pct = ((price - avg) / avg * 100) if avg > 0 else 0

    return {
        'name': key,
        'price': f'{price:.2f}',
        'pricecur': f'{price:.2f} {target_cur or cur}',
        'cur': target_cur or cur,
        'pct': f'{sgn(pct)}{pct:.2f}%',
        'change': f'{sgn(change)}{change:.2f}',
        'wert': f'{price * anzahl:.2f}',
        'profit': f'{sgn(profit)}{profit:.2f}',
        'profitpct': f'{sgn(profit_pct)}{profit_pct:.2f}%',
        'state': market_state(),
        'debug': f'{key} state={market_state()} price={price:.4f} prev={prev:.4f} cur={target_cur or cur}',
    }


def parse_positions(raw):
    """p=MSTR:2:100,EUROPE:3:90:CHF  ->  [(sym, anzahl, avg, cur), ...]"""
    for item in raw.split(','):
        if not item.strip():
            continue
        parts = (item.split(':') + ['', '', ''])[:4]
        try:
            anzahl = float(parts[1]) if parts[1].strip() else 0.0
            avg = float(parts[2]) if parts[2].strip() else 0.0
        except ValueError:
            anzahl = avg = 0.0
        yield parts[0].strip().upper(), anzahl, avg, parts[3].strip().upper()


def rows_for(raw):
    out = []
    for key, anzahl, avg, cur in parse_positions(raw):
        try:
            out.append(values(key, anzahl, avg, cur))
        except Exception:
            leer = {k: '—' for k in ('price', 'pricecur', 'cur', 'pct',
                                     'change', 'wert', 'profit', 'profitpct')}
            leer['name'] = key
            out.append(leer)
    return out


def plain(body):
    return Response(body, mimetype='text/plain; charset=utf-8')


@app.route('/')
def index():
    field = request.args.get('f', 'price')
    positions = request.args.get('p', '')

    try:
        if field in ('table', 'list') and positions:
            rows = rows_for(positions)

            if field == 'list':
                col = request.args.get('col', 'pricecur')
                return plain('\n'.join(r.get(col, '—') for r in rows))

            cols = request.args.get('cols', 'name,pricecur,profitpct').split(',')
            widths = [max(len(r.get(c, '—')) for r in rows) for c in cols]
            lines = []
            for r in rows:
                cells = [r.get(c, '—').ljust(widths[i]) if i == 0 else r.get(c, '—').rjust(widths[i])
                         for i, c in enumerate(cols)]
                lines.append('  '.join(cells).rstrip())
            return plain('\n'.join(lines))

        key = request.args.get('s', 'MSTR').upper()
        anzahl = float(request.args.get('a', 0))
        avg = float(request.args.get('avg', 0))
        target_cur = request.args.get('cur', '').upper()
        vals = values(key, anzahl, avg, target_cur)
        return plain(vals.get(field, vals['price']))
    except Exception:
        return plain('—')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
