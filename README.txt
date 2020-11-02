# setup
    pip install -r requirements.txt
    python3 main.py init-db
# run
    python3 main.py run-puller
    python3 main.py prepare btcpln
# testing
    pytest -vs
    pytest -vs -m "not slow"