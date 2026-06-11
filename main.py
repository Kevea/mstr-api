from flask import Flask, request
import requests

app = Flask(__name__)

def get_mstr():
    r = requests.get(
        'https://query1.finance.yahoo.com/v8/finance/chart/MSTR',
        headers={'User-Agent': 'Mozilla/5.0'}
    )
    meta = r.json()['chart']['result'][0]['meta']
    
    regular = meta['regularMarketPrice']
    prev    = meta['chartPreviousClose']
    pre     = meta.get('preMarketPrice', None)
    post    = meta.get('postMarketPrice', None)
    state   = meta.get('marketState', 'CLOSED')
    
    # Auto-switch: Pre/Post Market oder Regular
    if state == 'PRE' and pre:
        price = pre
    elif state in ('POST', 'POSTPOST') and post:
        price = post
    else:
        price = regular
    
    return price, prev, regular, state

@app.route('/')
def index():
    field  = request.args.get('f', 'price')
    anzahl = float(request.args.get('a', 0))
    avg    = float(request.args.get('avg', 0))
    try:
        price, prev, regular, state = get_mstr()
        change     = price - prev
        pct        = (change / prev) * 100
        profit_usd = (price - avg) * anzahl
        profit_pct = ((price - avg) / avg * 100) if avg > 0 else 0
        wert       = price * anzahl

        if field == 'price':     return f"{price:.2f}"
        if field == 'pct':       return f"{'+' if pct>=0 else ''}{pct:.2f}%"
        if field == 'change':    return f"{'+' if change>=0 else ''}{change:.2f}"
        if field == 'wert':      return f"{wert:.2f}"
        if field == 'profit':    return f"{'+' if profit_usd>=0 else ''}{profit_usd:.2f}"
        if field == 'profitpct': return f"{'+' if profit_pct>=0 else ''}{profit_pct:.2f}%"
        if field == 'state':     return state
        return f"{price:.2f}"
    except:
        return 'Error'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
