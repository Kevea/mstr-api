from flask import Flask, request
import requests

app = Flask(__name__)

@app.route('/')
def get_data():
    field = request.args.get('f', 'price')
    try:
        r = requests.get(
            'https://query1.finance.yahoo.com/v8/finance/chart/MSTR',
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        meta = r.json()['chart']['result'][0]['meta']
        price = meta['regularMarketPrice']
        prev  = meta['chartPreviousClose']
        change = round(price - prev, 2)
        pct    = round((change / prev) * 100, 2)

        if field == 'price': return str(round(price, 2))
        if field == 'change': return f"{'+' if change >= 0 else ''}{change}"
        if field == 'pct': return f"{'+' if pct >= 0 else ''}{pct}%"
        return str(round(price, 2))
    except:
        return 'Error'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
