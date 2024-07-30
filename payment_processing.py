from web3 import Web3
import json
from db_operations import create_connection, insert_payment

infura_url = "https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID"
web3 = Web3(Web3.HTTPProvider(infura_url))
database = "payments.db"

def generate_wallet():
    account = web3.eth.account.create()
    return {
        'address': account.address,
        'private_key': account.private_key.hex()
    }

def send_transaction(from_address, private_key, to_address, amount):
    conn = create_connection(database)
    tx = {
        'nonce': web3.eth.getTransactionCount(from_address),
        'to': to_address,
        'value': web3.toWei(amount, 'ether'),
        'gas': 2000000,
        'gasPrice': web3.toWei('50', 'gwei'),
    }
    signed_tx = web3.eth.account.sign_transaction(tx, private_key=private_key)
    tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
    insert_payment(conn, (from_address, to_address, amount, tx_hash.hex()))
    return tx_hash.hex()
