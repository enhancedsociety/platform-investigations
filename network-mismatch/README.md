# Example of network mismatch handling

Implements a website to identify Ethereum network and protect against mismatch by redirecting or asking users to switch metamask connection.

```

python3 -m virtualenv venv

source venv/bin/activate

pip install web3 Flask

FLASK_DEBUG=1 FLASK_APP=main.py python -m flask run
```