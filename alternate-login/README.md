# Example of login without Metamask or integrated providers

Implements a minimal, safe login mechanism that requires direct user input of eth credentials. It can be useful for inexperienced users or users without access to the metamask extension (Safari, basically) or a Dapp enabled browser (such as Brave of Toshi).


```

python3 -m virtualenv -p python3 venv

source venv/bin/activate

pip install web3 Flask eth-account==0.1.0a2

FLASK_DEBUG=1 FLASK_APP=main.py python -m flask run
```