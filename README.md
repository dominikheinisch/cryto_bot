# crypto_bot

## 1. requirements
```
pip3 install -r requirements.txt
```

## 2. setup
```
python3 main.py init-db
```

## 3. data puller
pulls data from bitbay, eg. https://bitbay.net/API/Public/btcpln/trades.json?since=0
```
python3 main.py run-puller
```

## 4. data pre-processing
```
python3 main.py prepare btcpln                 # btcpln, ethpln, btgpln, etc...
```

## 5. testing
```
python3 -m pytest -vs                                     # run all
python3 -m pytest -vs -m "not slow"                       # run all except slow tests
```
