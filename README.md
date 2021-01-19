# crypto_bot

[![Build Status](https://github.com/dominikheinisch/cryto_bot/workflows/Python%20package/badge.svg)](https://github.com/dominikheinisch/cryto_bot/actions?query=workflow%3A"Python+package")
[![Build Status](https://github.com/dominikheinisch/cryto_bot/workflows/docker-compose%20CI/badge.svg)](https://github.com/dominikheinisch/cryto_bot/actions?query=workflow%3A%22docker-compose+CI%22")

## 1. requirements
```
pip3 install -r requirements.txt
```

## 2. setup
```
pip3 install -e .                                         # package instalation
pip3 show crypto_bot                                      # show package info
python3 crypto_bot init-db
```

## 3. data puller
pulls data from bitbay, eg. https://bitbay.net/API/Public/btcpln/trades.json?since=0
```
python3 -m crypto_bot run-puller
```

## 4. data pre-processing
```
python3 -m crypto_bot prepare btgpln                      # btcpln, ethpln, btgpln, etc...
```

## 5. testing
```
python3 -m pytest -vs                                     # run all
python3 -m pytest -vs -m "not slow"                       # run all except slow tests
```

## 6. pip installation
```
pip3 install -e git+https://github.com/dominikheinisch/cryto_bot@main#egg=cryto_bot
```
