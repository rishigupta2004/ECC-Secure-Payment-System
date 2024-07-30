from tinydb import TinyDB, Query

db = TinyDB('database.json')

def initialize_db():
    db.truncate()  # Clear the database

def register_user(user_id, private_key, public_key):
    User = Query()
    if db.search(User.user_id == user_id):
        return False
    db.insert({'user_id': user_id, 'private_key': private_key, 'public_key': public_key})
    return True

def find_user(user_id):
    User = Query()
    return db.get(User.user_id == user_id)

def save_transaction(from_user_id, to_user_id, amount, signature, transaction_details):
    return db.insert({'from_user_id': from_user_id, 'to_user_id': to_user_id, 'amount': amount, 'signature': signature, 'transaction_details': transaction_details})

def get_transactions():
    return db.all()
