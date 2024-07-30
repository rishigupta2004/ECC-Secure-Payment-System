from flask import Flask, request, jsonify
from db_operations import register_user, find_user, save_transaction, get_transactions, initialize_db
from crypto_utils import generate_key_pair, sign_transaction, verify_signature

app = Flask(__name__)
initialize_db()

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    user_id = data.get('user_id')
    
    # Generate ECC key pair
    private_key, public_key = generate_key_pair()
    
    # Save keys and user_id in database
    if register_user(user_id, private_key, public_key):
        return jsonify({
            'user_id': user_id,
            'public_key': public_key,
            'private_key': private_key
        }), 201
    else:
        return jsonify({'error': 'User already exists'}), 400

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user_id = data.get('user_id')
    
    user = find_user(user_id)
    if user:
        return jsonify({
            'user_id': user['user_id'],
            'public_key': user['public_key'],
            'private_key': user['private_key']
        }), 200
    else:
        return jsonify({'error': 'User not found'}), 404

@app.route('/send_transaction', methods=['POST'])
def send_transaction():
    data = request.json
    from_user_id = data.get('from_user_id')
    to_user_id = data.get('to_user_id')
    amount = data.get('amount')
    
    from_user = find_user(from_user_id)
    to_user = find_user(to_user_id)
    
    if not from_user or not to_user:
        return jsonify({'error': 'User not found'}), 404
    
    # Create transaction details
    transaction_details = f"{from_user_id} -> {to_user_id}: {amount}"
    
    # Sign transaction with sender's private key
    private_key = from_user['private_key']
    signature = sign_transaction(private_key, transaction_details)
    
    # Save transaction in the database
    transaction_id = save_transaction(from_user_id, to_user_id, amount, signature, transaction_details)
    
    return jsonify({'message': 'Transaction successful', 'signature': signature, 'transaction_id': transaction_id}), 200

@app.route('/transactions', methods=['GET'])
def transactions():
    transactions = get_transactions()
    return jsonify(transactions), 200

if __name__ == '__main__':
    app.run(debug=True)
