import requests

def get_data(currencies, category, since=0):
    session = requests.Session()
    data = session.get(f'https://bitbay.net/API/Public/{currencies}/{category}.json?since={since}')
    return data.json()

def get_btcpln_trades(since=0):
    return get_data(currencies='btcpln', category='trades', since=since)

def get_first_100_btcpln():
    for i in (50 * i for i in range(100)):
        print(i)
        trade_data(get_btcpln_trades(since=i))

def trade_data(data):
    for item in data:
        date = item['date']
        price = item['price']
        amount = item['amount']
        tid = item['tid']
        print(tid, price, amount, date)

if __name__ == '__main__':
    get_first_100_btcpln()
