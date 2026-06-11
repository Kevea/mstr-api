from flask import Flask, request
import requests

app = Flask(__name__)

def get_price():
    # Versuche Nasdaq API für Pre/Post Market
    try:
        r = requests.get(
            'https://api.nasdaq.com/api/quote/MSTR/info?assetclass=stocks',
            headers={
                'User-Agent': 'Mozilla/5.0',
                'Accept': 'application/json'
            }
        )
        data = r.json()['data']
        state = data.get('marketStatus', 'Closed')
        regular = float(data['primaryData']['lastSalePrice'].replace('$','').replace(',',''))
        
        pre  = data.get('secondaryData', {})
        pre_price = pre.get('lastSalePrice', '$0').replace('$','').replace(',','')
        pre_price = float(pre_price) if pre_price else 0
        
        if 'Pre' in state and pre_price > 0:
            return pre_price, regular, regular, state
        return regular, regular, regular, state
    except:
        # Fallback Yahoo
        r = requests.get(
            'https://query1.finance.yahoo.com/v8/finance/chart/MSTR',
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        meta = r.json()['chart']['result'][0]['meta']
        regular = meta.get('regularMarketPrice', 0)
        prev = meta.get('chartPreviousClose', regular)
        return regular, prev, regular, 'REGULAR'

@app.route('/')
def index():
    field  = request.args.get('f', 'price')
    anzahl = float(request.args.get('a', 0))
    avg    = float(request.args.get('avg', 0))
    try:
        price, prev, regular, state = get_price()
        change     = price - prev
        pct        = (change / prev) * 100
        profit_usd = (price - avg) * anzahl
        profit_pct = ((price - avg) / avg * 100) if avg > 0 else 0
        wert       = price * anzahl

        if field == 'debug':     return f"state={state} price={price} prev={prev}"
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
