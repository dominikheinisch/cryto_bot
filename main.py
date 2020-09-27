import requests
import time

def get_data(symbol, category, since):
    session = requests.Session()
    data = session.get(f'https://bitbay.net/API/Public/{symbol}/{category}.json?since={since}')
    return data.json(), symbol

def get_trades(symbol, since=0):
    return get_data(symbol=symbol, category='trades', since=since)

def get_first_n_btcpln(n):
    TRADES_SIZE = 50
    start_time = time.time()
    for i in (TRADES_SIZE * i - 1 for i in range(n)):
        trade_data(*get_trades(symbol='btcpln', since=i))
        print(time.time() - start_time)

def trade_data(data, symbol):
    for item in data:
        date = item['date']
        price = item['price']
        amount = item['amount']
        tid = item['tid']
        print(tid, price, amount, symbol, date)

if __name__ == '__main__':
    get_first_n_btcpln(n=10000)
