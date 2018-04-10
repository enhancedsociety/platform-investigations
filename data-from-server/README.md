# Example of platform fully served from server

Implements a minimal project dashboard with all data (including on-chain) served from the server.


```
python3 -m virtualenv -p python3 venv

source venv/bin/activate

pip install web3 Flask eth-account==0.1.0a2 shove

FLASK_DEBUG=1 FLASK_APP=main.py python -m flask run
```

## Contracts

There are 3 types of contracts defined:
 - Platform, which represents the platform where ICOs are published and users interact with them
 - Token, a *very* simple fixed supply ERC20 token to be deployed with each project.
 - ICO, the initial holder of a projects tokens, with specific intructions to dole out the tokens (just plain "x money for y tokens" in this case).

 The platform has references to all of the others, and there is a platform deployment on ropsten (so this toy project has a reference on-chain) at [0xE995620249f762FB81CD88eB0Fb02Bc460de6952](https://ropsten.etherscan.io/address/0xE995620249f762FB81CD88eB0Fb02Bc460de6952)