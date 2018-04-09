# Example of network mismatch handling

Implements a website to identify Ethereum network and protect against mismatch by redirecting or asking users to switch metamask connection.

```

python3 -m virtualenv -p python3 venv

source venv/bin/activate

pip install web3 Flask eth-account==0.1.0a2

FLASK_DEBUG=1 FLASK_APP=main.py python -m flask run
```