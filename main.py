from flask import Flask, request
import requests

app = Flask(__name__)

@app.route('/')
def index():
    field = request.args.get('f', 'price')
    anzahl = float(request.args.get('a', 0))
    avg = float(request.args.get('avg', 0))
    try:
        r = requests.get(
            'https://query1.finance.yahoo.com/v8/finance/chart/MSTR',
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        meta = r.json()['chart']['result'][0]['meta']
        
        regular    = meta.get('regularMarketPrice', 0)
        prev       = meta.get('chartPreviousClose', regular)
        pre        = meta.get('preMarketPrice', 0)
        post       = meta.get('postMarketPrice', 0)
        state      = meta.get('marketState', 'CLOSED')

        # Debug — zeigt alle Werte
        if field == 'debug':
            return f"state={state} regular={regular} pre={pre} post={post}"

        # Auto-switch
        if state == 'PRE' and pre > 0:
            price = pre
        elif state in ('POST','POSTPOST') and post > 0:
            price = post
        else:
            price = regular

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
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
