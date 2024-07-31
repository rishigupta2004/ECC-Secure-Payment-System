from flask import Flask, request, jsonify
from db_operations import register_user, login_user, send_transaction, get_transactions, initialize_db
import logging

app = Flask(__name__)

# Initialize the database
initialize_db()

# Set up logging
logging.basicConfig(level=logging.DEBUG)

@app.route('/login', methods=['POST'])
def login():
    user_id = request.json.get('user_id')
    logging.debug(f"Login attempt for user_id: {user_id}")
    user_data = login_user(user_id)
    if user_data:
        return jsonify(user_data), 200
    else:
        logging.error("Login failed for user_id: %s", user_id)
        return jsonify({'error': 'Login failed'}), 400

@app.route('/send_transaction', methods=['POST'])
def transaction():
    data = request.json
    from_user_id = data.get('from_user_id')
    private_key = data.get('private_key')
    to_user_id = data.get('to_user_id')
    amount = data.get('amount')

    logging.debug(f"Transaction request from {from_user_id} to {to_user_id} of amount {amount}")
    
    result = send_transaction(from_user_id, to_user_id, amount, private_key)
    logging.debug(f"Transaction result: {result}")
    
    if 'error' in result:
        logging.error(f"Transaction error: {result['error']}")
        return jsonify(result), 400
    else:
        return jsonify(result), 200

@app.route('/transactions', methods=['GET'])
def transactions():
    transactions = get_transactions()
    return jsonify(transactions), 200

if __name__ == '__main__':
    app.run(debug=True)
