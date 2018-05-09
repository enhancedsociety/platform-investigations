from flask import Flask, request, abort, render_template, jsonify
from web3 import Web3, HTTPProvider

w3 = {
    'mainnet': Web3(HTTPProvider('https://mainnet.infura.io/')),
    'ropsten': Web3(HTTPProvider('https://ropsten.infura.io/')),
    'kovan': Web3(HTTPProvider('https://kovan.infura.io/')),
    'rinkeby': Web3(HTTPProvider('https://rinkeby.infura.io/')),
}

app = Flask(__name__)

@app.route('/', methods=["GET"])
def index():
    return render_template('index.html')


@app.route('/<network_name>', methods=["GET"])
def ethnet(network_name):
    if network_name in w3:
        network_id = w3[network_name].version.network
        return render_template('network_specific.j2', network_name=network_name, network_id=network_id)
    else:
        return abort(404)


