from flask import Flask, session, redirect, url_for, escape, request, abort, render_template, jsonify
from functools import wraps
from random import randint
from web3.auto import w3

w3.eth.enable_unaudited_features()


def needs_auth(func):
    """Checks whether user is logged in or raises error 401."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if is_logged_in():
            return func(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    return wrapper


def is_logged_in():
    msg = '{}|{}'.format(
        request.headers['Host'], CHALLENGE_STORE.get(session.get('address', ''), ''))
    return 'signed_token' in session and verify_signature(msg, session['signed_token'])


def verify_signature(token, signed_token):
    r = w3.eth.account.recoverMessage(
        text=token, signature=signed_token).lower()
    addr = session.get('address', '').lower()
    return addr.startswith('0x') and r == addr


app = Flask(__name__)
# set the secret key.  keep this really secret:
app.secret_key = 'manamana'

CHALLENGE_STORE = dict()


@app.route('/')
def index():
    if is_logged_in():
        return '<p>Hello {}</p> <a href="/logout">Sign out</a>'.format(escape(session['address']))
    return '<p>You are not logged in</p> <a href="/login">Sign in</a>'


@app.route('/inner')
@needs_auth
def inner():
    return 'If you are not logged in, you shouldn\'t see this'


@app.route('/login', methods=['GET', 'POST'])
def login():
    if is_logged_in():
        return redirect(url_for('index'))
    if request.method == 'POST':
        form_data = request.get_json(force=True)
        if 'address' in session and 'signed_token' in form_data:
            msg = '{}|{}'.format(
                request.headers['Host'], CHALLENGE_STORE.get(session['address'], str()))
            verified = verify_signature(msg, form_data.get('signed_token', ''))
            if verified:
                session['signed_token'] = form_data['signed_token']
                return 'OK'
            else:
                return abort(401)
        else:
            return abort(400)
    return render_template('login.html')


@app.route('/token/<address>', methods=['GET'])
def login_challenge(address):
    session['address'] = address
    token = str(randint(1, 1_000_000_000))
    CHALLENGE_STORE[address] = token
    return jsonify({"token": token})


@app.route('/logout')
def logout():
    session.pop('address', None)
    session.pop('signed_token', None)
    return redirect(url_for('index'))
