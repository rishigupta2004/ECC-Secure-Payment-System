
from tinydb import TinyDB, Query
import hashlib
from ecdsa import SigningKey, SECP256k1
import logging
import sqlite3
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# TinyDB setup
db = TinyDB('database.json')

# SQLite setup
conn = sqlite3.connect('payments.db')
cursor = conn.cursor()

def initialize_db():
    # TinyDB initialization
    db.drop_tables()
    db.table('users')
    db.table('transactions')

    # SQLite initialization
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT NOT NULL,
        private_key TEXT NOT NULL,
        public_key TEXT NOT NULL
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        from_user_id TEXT NOT NULL,
        to_user_id TEXT NOT NULL,
        amount REAL NOT NULL,
        signature TEXT NOT NULL,
        transaction_details TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    conn.commit()

def register_user(user_id):
    private_key = SigningKey.generate(curve=SECP256k1)
    public_key = private_key.get_verifying_key()

    # TinyDB insertion
    users_table = db.table('users')
    users_table.insert({
        'user_id': user_id,
        'private_key': private_key.to_string().hex(),
        'public_key': public_key.to_string().hex()
    })

    # SQLite insertion
    cursor.execute('''
    INSERT INTO users (user_id, private_key, public_key) VALUES (?, ?, ?)
    ''', (user_id, private_key.to_string().hex(), public_key.to_string().hex()))
    conn.commit()

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
    try:
        users_table = db.table('users')
        from_user = users_table.get(Query().user_id == from_user_id)
        to_user = users_table.get(Query().user_id == to_user_id)

        if not from_user:
            logging.error(f"User {from_user_id} not found")
            return {'error': 'Sender not found'}
        if not to_user:
            logging.error(f"User {to_user_id} not found")
            return {'error': 'Receiver not found'}

        # Validate private key
        private_key = SigningKey.from_string(bytes.fromhex(private_key_hex), curve=SECP256k1)
        if private_key.to_string().hex() != from_user['private_key']:
            logging.error("Invalid private key")
            return {'error': 'Invalid private key'}

        transaction_details = f"{from_user_id} -> {to_user_id}: {amount}"
        signature = private_key.sign(transaction_details.encode())

        # TinyDB insertion
        transactions_table = db.table('transactions')
        transactions_table.insert({
            'from_user_id': from_user_id,
            'to_user_id': to_user_id,
            'amount': amount,
            'signature': signature.hex(),
            'transaction_details': transaction_details
        })

        # SQLite insertion
        cursor.execute('''
        INSERT INTO transactions (from_user_id, to_user_id, amount, signature, transaction_details) VALUES (?, ?, ?, ?, ?)
        ''', (from_user_id, to_user_id, amount, signature.hex(), transaction_details))
        conn.commit()

        logging.info("Transaction successful")
        return {
            'message': 'Transaction successful',
            'signature': signature.hex()
        }
    except Exception as e:
        logging.error(f"An error occurred during the transaction: {e}")
        return {"error": str(e)}

def get_transactions():
    # TinyDB transactions
    transactions_table = db.table('transactions')
    json_transactions = transactions_table.all()

    # SQLite transactions
    cursor.execute('SELECT * FROM transactions')
    db_transactions = cursor.fetchall()

    all_transactions = json_transactions + [
        {
            'from_user_id': row[1],
            'to_user_id': row[2],
            'amount': row[3],
            'signature': row[4],
            'transaction_details': row[5],
            'timestamp': row[6]
        } for row in db_transactions
    ]
    return all_transactions
