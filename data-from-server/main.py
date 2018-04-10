from flask import Flask, session, redirect, url_for, escape, request, abort, render_template, jsonify
from functools import wraps
from random import randint
from collections import namedtuple
import web3
from web3 import Web3, HTTPProvider
from shove import Shove

from contract_data import PLATFORM_ABI, PLATFORM_BYTECODE, TOKEN_ABI, TOKEN_BYTECODE, ICO_ABI, ICO_BYTECODE

w3 = Web3(HTTPProvider('https://ropsten.infura.io/***REMOVED***'))
#w3 = Web3(HTTPProvider('http://localhost:8545'))

w3.eth.enable_unaudited_features()

##########
# DANGER
#
# THE FOLLOWING SHOULD NEVER BE IN THE CODE BUT RATHER
# BE READ FROM A CONFIG FILE OR ENVIRONMENT VARIABLE.
# THESE ARE MEANINGLESS AS THEY ARE ONLY BOUND TO A TEST/DEMO
# DEPLOYMENT. IF YOU WISH TO EXPERIMENT MORE SERIOUSLY,
# REDEPLOY THE PLATFORM AND START OVER
#
##########
# Deployment of new projects is still manual, use this key
# PLATFORM_OWNER_PRIVKEY = '0x8d4ee24d8d99220a91252ac22262562b6db07ae8375878b56868c0ffa7d43c2e'

PLATFORM_ADDRESS = Web3.toChecksumAddress(
    '0x9C7Da6Bd482C724449ceA8497D4f86f090DbA80e')

# if w3.eth.getCode(PLATFORM_ADDRESS) == b'\x00':
#    platform_contract = w3.eth.contract(
#        abi=PLATFORM_ABI, bytecode=PLATFORM_BYTECODE)
#    tx_hash = platform_contract.deploy(
#        transaction={'from': w3.eth.accounts[0], 'gas': 4000000})
#    print('TXHASH {}'.format(tx_hash))
#    txn_receipt = w3.eth.getTransactionReceipt(tx_hash)
#    print('TXRECEIPT {}'.format(txn_receipt))
#    PLATFORM_ADDRESS = txn_receipt['contractAddress']

platform_contract = w3.eth.contract(address=PLATFORM_ADDRESS, abi=PLATFORM_ABI)
##########


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

CHALLENGE_STORE = Shove('file://user_session_challenge')


@app.route('/login', methods=['GET', 'POST'])
def login():
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
    session['address'] = Web3.toChecksumAddress(address)
    token = str(randint(1, 1_000_000_000))
    CHALLENGE_STORE[session['address']] = token
    CHALLENGE_STORE.sync()
    return jsonify({"token": token})


@app.route('/logout')
def logout():
    addr = session.pop('address', None)
    session.pop('signed_token', None)
    CHALLENGE_STORE.pop(addr)
    CHALLENGE_STORE.sync()
    return redirect(url_for('index'))


@app.route('/')
def index():
    user = session['address'] if is_logged_in() else None
    return render_template('landing.html', user=user)


@app.route('/dashboard')
@needs_auth
def dashboard():
    Project = namedtuple(
        'Project', ['name', 'symbol', 'ico_address', 'token_address', 'platform_idx'])
    n_proj = platform_contract.functions.numProjects().call()
    other_projects = list()
    invest_projects = list()
    for i in range(n_proj):
        name, tok_addr, ico_addr = platform_contract.functions.getProject(
            i).call()
        token_contract = w3.eth.contract(address=tok_addr, abi=TOKEN_ABI)
        token_symbol = token_contract.call().symbol()
        user_balance = token_contract.functions.balanceOf(
            session['address']).call()
        p = Project(name, token_symbol, ico_addr, tok_addr, i)
        if user_balance > 0:
            invest_projects.append(p)
        else:
            other_projects.append(p)
    return render_template('dashboard.html', user=session['address'], invest_projects=invest_projects, other_projects=other_projects)


@app.route('/project/create')
@needs_auth
def create():
    return render_template('create.html', user=session['address'], platform_contract=PLATFORM_ADDRESS, platform_abi=PLATFORM_ABI, token_b=TOKEN_BYTECODE, token_abi=TOKEN_ABI, ico_b=ICO_BYTECODE, ico_abi=ICO_ABI)


@app.route('/project/<int:n>')
@needs_auth
def project_details(n):
    n_proj = platform_contract.functions.numProjects().call()
    if n < 0 or n >= n_proj:
        return abort(404)

    ICO = namedtuple('ICO', ['address', 'balance', 'price', 'funds'])
    Token = namedtuple('Token', ['address', 'name', 'symbol', 'supply'])

    _, tok_addr, ico_addr = platform_contract.functions.getProject(n).call()

    token_contract = w3.eth.contract(address=tok_addr, abi=TOKEN_ABI)
    token_symbol = token_contract.call().symbol()
    token_name = token_contract.call().name()
    token_supply = token_contract.call().totalSupply()
    t = Token(tok_addr, token_name, token_symbol, token_supply)

    user_balance = token_contract.functions.balanceOf(
        session['address']).call()

    ico_contract = w3.eth.contract(address=ico_addr, abi=ICO_ABI)
    ico_balance = token_contract.functions.balanceOf(ico_addr).call()
    ico_funds = w3.eth.getBalance(ico_addr)
    ico_price = ico_contract.call().tokenPriceInWei()
    ico = ICO(ico_addr, ico_balance, ico_price, ico_funds)

    return render_template('project.html', user=session['address'], token=t, ico=ico, user_balance=user_balance)


@app.route('/profile')
@needs_auth
def profile():
    return render_template('profile.html', user=session['address'])
