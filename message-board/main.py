from collections import namedtuple
from flask import Flask, session, redirect, url_for, escape, request, abort, render_template, jsonify
from web3 import Web3
from web3.auto import w3

w3.eth.enable_unaudited_features()

app = Flask(__name__)

messages = list()

Message = namedtuple('Message', ['message', 'signature', 'author'])


@app.route('/')
def index():
    return render_template('index.html', messages=messages)


def verify_sig(msg, sig, addr):
    recovered_addr = w3.eth.account.recoverMessage(text=msg, signature=sig)
    return Web3.toChecksumAddress(addr) == Web3.toChecksumAddress(recovered_addr)


@app.route('/post', methods=['POST'])
def post():
    if request.method == 'POST':
        form_data = request.get_json(force=True)
        if 'message' in form_data \
            and 'signature' in form_data \
                and 'author' in form_data \
                and verify_sig(form_data['message'], form_data['signature'], form_data['author']):
            messages.append(
                Message(form_data['message'], form_data['signature'], form_data['author']))
            return jsonify({'ok': True})
    return abort(400)
