# Example of a message board

Implements a one page message board with cryptographically verified message authors. All crypto/web3 interaction is done client-side. Server is a dumb object store/template renderer.


```

python3 -m virtualenv -p python3 venv

source venv/bin/activate

pip install Flask

FLASK_DEBUG=1 FLASK_APP=main.py python -m flask run
```