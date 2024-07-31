import json

def load_database():
    with open('database.json', 'r') as db_file:
        return json.load(db_file)

def save_database(database):
    with open('database.json', 'w') as db_file:
        json.dump(database, db_file, indent=4)

def perform_transaction(from_user, private_key, to_user, amount):
    database = load_database()
    
    # Debugging print statements
    print(f"From User: {from_user}")
    print(f"Private Key: {private_key}")
    print(f"To User: {to_user}")
    print(f"Amount: {amount}")

    if from_user not in database:
        return "Transaction failed: Sender does not exist."

    if to_user not in database:
        return "Transaction failed: Receiver does not exist."

    sender = database[from_user]
    receiver = database[to_user]

    # Validate private key (for simplicity, assuming it matches exactly)
    if sender['private_key'] != private_key:
        return "Transaction failed: Invalid private key."

    # Check if sender has enough balance
    if sender['balance'] < amount:
        return "Transaction failed: Insufficient funds."

    # Perform the transaction
    sender['balance'] -= amount
    receiver['balance'] += amount

    save_database(database)
    return "Transaction successful."

# Example usage
if __name__ == "__main__":
    from_user = "rishigupta.rg007@gmail.com"
    private_key = "3873f720703f46c1b6553b9291480b4511be7a684a6348e44117f98c6ca429d4"
    to_user = "akarshannagpal@gmail.com"
    amount = 10000
    result = perform_transaction(from_user, private_key, to_user, amount)
    print(result)
