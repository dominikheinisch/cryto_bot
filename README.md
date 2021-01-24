# crypto_bot

[![Build Status](https://github.com/dominikheinisch/cryto_bot/workflows/Python%20package/badge.svg)](https://github.com/dominikheinisch/cryto_bot/actions?query=workflow%3A"Python+package")
[![Build Status](https://github.com/dominikheinisch/cryto_bot/workflows/docker-compose%20CI/badge.svg)](https://github.com/dominikheinisch/cryto_bot/actions?query=workflow%3A%22docker-compose+CI%22")

## 1. requirements
```
docker-compose version 3.7
```

## 2. setup
```
docker-compose build
docker-compose run crypto_bot python3 -m src init-db
```

## 3. data puller
pulls data from bitbay, eg. https://bitbay.net/API/Public/btcpln/trades.json?since=0
```
docker-compose up --build
# or
docker-compose run crypto_bot python3 -m src run-puller
```

## 4. data pre-processor
```
docker-compose run crypto_bot python3 -m src prepare lskpln     # btcpln, ethpln, btgpln, etc...
```

## 5. testing
```
docker-compose run crypto_bot pytest -v                         # run all
docker-compose run crypto_bot pytest -v -m "not slow"           # run all except slow tests
```

## 6. testing on local machine
```
pip3 install -r crypto_bot/requirements.txt
python3 -m pytest -vvs crypto_bot
```
