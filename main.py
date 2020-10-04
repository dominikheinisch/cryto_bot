import requests
import time

def get_data(symbol, category, since):
    session = requests.Session()
    data = session.get(f'https://bitbay.net/API/Public/{symbol}/{category}.json?since={since}')
    return data.json(), symbol

def get_trades(symbol, since):
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

def process_data(data):
    pass

def pull_trades(symbol):
    TRADES_SIZE = 50
    # TODO
    # if symbol in db
    # since = db.getSince
    # else
    # insert to DB
    # since = -1
    since = 8212602
    is_empty = False
    start_time = time.time()
    while(not is_empty):
        data, symbol = get_data(symbol=symbol, category='trades', since=since)
        trade_data(data, symbol)
        is_empty = not len(data)
        since += TRADES_SIZE
        print(time.time() - start_time)

def pull_all_trades(symbols=['btcpln', 'lskpln']):
    for symbol in symbols:
        pull_trades(symbol)

if __name__ == '__main__':
    # get_first_n_btcpln(n=10000)
    while(True):
        pull_all_trades()
        time.sleep(10)
