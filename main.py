from flask import Flask, request
import requests

app = Flask(__name__)

FINNHUB_KEY = "d8l7pehr01qut1f9kk8gd8l7pehr01qut1f9kk90"

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

        if field == 'debug':     return f"price={price} prev={prev}"
        if field == 'price':     return f"{price:.2f}"
        if field == 'pct':       return f"{'+' if pct>=0 else ''}{pct:.2f}%"
        if field == 'change':    return f"{'+' if change>=0 else ''}{change:.2f}"
        if field == 'wert':      return f"{wert:.2f}"
        if field == 'profit':    return f"{'+' if profit_usd>=0 else ''}{profit_usd:.2f}"
        if field == 'profitpct': return f"{'+' if profit_pct>=0 else ''}{profit_pct:.2f}%"
        return f"{price:.2f}"
    except Exception as e:
        return "—"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
