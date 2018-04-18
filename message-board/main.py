from collections import namedtuple
from flask import Flask, session, redirect, url_for, escape, request, abort, render_template, jsonify

app = Flask(__name__)

messages = list()

Message = namedtuple('Message', ['message', 'signature', 'author'])


@app.route('/')
def index():
    return render_template('index.html', messages=messages)


@app.route('/post', methods=['POST'])
def post():
    if request.method == 'POST':
        form_data = request.get_json(force=True)
        if 'message' in form_data and 'signature' in form_data and 'author' in form_data:
            # TODO
            # to avoid adding garbage to `messages`,
            # add web3 dependency and validate the address
            # prior to appending
            messages.append(
                Message(form_data['message'], form_data['signature'], form_data['author']))
            return jsonify({'ok': True})
    return abort(400)
