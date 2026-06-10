from flask import Flask
import requests

app = Flask(__name__)

@app.route('/')
def get_price():
    try:
        r = requests.get(
            'https://query1.finance.yahoo.com/v8/finance/chart/MSTR',
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        price = r.json()['chart']['result'][0]['meta']['regularMarketPrice']
        return str(round(price, 2))
    except:
        return 'Error'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
