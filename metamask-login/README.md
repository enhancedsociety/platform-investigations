# Example of login with Metamask

Implements a minimal, safe login mechanism that integrates with metamask.


```

python3 -m virtualenv venv

source venv/bin/activate

pip install web3 Flask

FLASK_DEBUG=1 FLASK_APP=main.py python -m flask run
```