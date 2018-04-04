# Example of login without Metamask or integrated providers

Implements a minimal, safe login mechanism that requires direct user input of eth credentials.


### Under construction

The signing code is still, currently, broken.


```

python3 -m virtualenv venv

source venv/bin/activate

pip install web3 Flask

FLASK_DEBUG=1 FLASK_APP=main.py python -m flask run
```