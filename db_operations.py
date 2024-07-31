from tinydb import TinyDB, Query
import hashlib
from ecdsa import SigningKey, VerifyingKey, SECP256k1

db = TinyDB('database.json')

def initialize_db():
    db.drop_tables()
    db.table('users')
    db.table('transactions')

def register_user(user_id):
    private_key = SigningKey.generate(curve=SECP256k1)
    public_key = private_key.get_verifying_key()

    users_table = db.table('users')
    users_table.insert({
        'user_id': user_id,
        'private_key': private_key.to_string().hex(),
        'public_key': public_key.to_string().hex()
    })
    
    return {
        'user_id': user_id,
        'public_key': public_key.to_string().hex(),
        'private_key': private_key.to_string().hex()
    }

def login_user(user_id):
    users_table = db.table('users')
    user = users_table.get(Query().user_id == user_id)
    if user:
        return {
            'user_id': user['user_id'],
            'public_key': user['public_key'],
            'private_key': user['private_key']
        }
    else:
        return register_user(user_id)

def send_transaction(from_user_id, to_user_id, amount, private_key_hex):
    users_table = db.table('users')
    from_user = users_table.get(Query().user_id == from_user_id)
    to_user = users_table.get(Query().user_id == to_user_id)
    
    if not from_user or not to_user:
        return {'error': 'User not found'}

    transaction_details = f"{from_user_id} -> {to_user_id}: {amount}"
    private_key = SigningKey.from_string(bytes.fromhex(private_key_hex), curve=SECP256k1)
    signature = private_key.sign(transaction_details.encode())

    transactions_table = db.table('transactions')
    transactions_table.insert({
        'from_user_id': from_user_id,
        'to_user_id': to_user_id,
        'amount': amount,
        'signature': signature.hex(),
        'transaction_details': transaction_details
    })
    
    return {
        'message': 'Transaction successful',
        'signature': signature.hex()
    }

def get_transactions():
    transactions_table = db.table('transactions')
    return transactions_table.all()
