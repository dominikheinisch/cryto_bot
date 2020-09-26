import requests
import time

def get_data(currencies, category, since=0):
    session = requests.Session()
    data = session.get(f'https://bitbay.net/API/Public/{currencies}/{category}.json?since={since}')
    return data.json(), currencies

def get_btcpln_trades(since=0):
    return get_data(currencies='btcpln', category='trades', since=since)

def get_first_n_btcpln(n):
    TRADES_SIZE = 50
    start_time = time.time()
    for i in (TRADES_SIZE * i - 1 for i in range(n)):
        trade_data(*get_btcpln_trades(since=i))
        print(time.time() - start_time)

def trade_data(data, currencies):
    for item in data:
        date = item['date']
        price = item['price']
        amount = item['amount']
        tid = item['tid']
        print(tid, price, amount, currencies, date)

if __name__ == '__main__':
    get_first_n_btcpln(n=10000)
