from flask import Flask, request, jsonify

app = Flask(__name__)

users = {
    "user1": {"password": "password1", "public_key": "public_key1", "private_key": "private_key1"},
    "user2": {"password": "password2", "public_key": "public_key2", "private_key": "private_key2"}
}

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user_id = data.get("user_id")
    password = data.get("password")
    
    user = users.get(user_id)
    if user and user["password"] == password:
        return jsonify({"public_key": user["public_key"], "private_key": user["private_key"]})
    else:
        return jsonify({"error": "Invalid credentials"}), 401

# Add your other endpoints here

if __name__ == '__main__':
    app.run(debug=True)
