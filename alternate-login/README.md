# Example of login without Metamask or integrated providers

Implements a minimal, safe login mechanism that requires direct user input of eth credentials.


### Under construction

The signing code is still, currently, broken.


```

python3 -m virtualenv -p python3 venv

source venv/bin/activate

pip install web3 Flask eth-account==0.1.0a2

FLASK_DEBUG=1 FLASK_APP=main.py python -m flask run
```