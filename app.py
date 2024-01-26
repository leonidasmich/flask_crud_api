from flask import Flask, request, jsonify
from flask_cors import CORS
from functools import wraps
import mysql.connector
from dotenv import load_dotenv
import os

app = Flask(__name__)
CORS(app)

# Token
load_dotenv()
AUTH_TOKEN = os.getenv('AUTH_TOKEN')

db_config = {
    'user': os.getenv('USER'),
    'password': os.getenv('PASSWORD'),
    'host': os.getenv('HOST'),
    'database': os.getenv('DATABASE')
}

# Function to get database connection
def get_db_connection():
    conn = mysql.connector.connect(**db_config)
    return conn

# Authorization Function
def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if token != AUTH_TOKEN:
            return jsonify({"message": "Invalid Token"}), 403
        return f(*args, **kwargs)
    return decorated_function


# Endpoint to show all users
@app.route('/users', methods=['GET'])
@token_required
def get_all_users():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    cursor.close()
    return jsonify(users)


# Endpoint to show one user by ID
@app.route('/users/<int:user_id>', methods=['GET'])
@token_required
def get_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    if user:
        return jsonify(user)
    else:
        return jsonify({"message": "User not found"}), 400


# Endpoint to delete a user by ID
@app.route('/users/<int:user_id>', methods=['DELETE'])
@token_required
def delete_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "User Deleted"})


# Endpoint to update a user by ID
@app.route('/users/<int:user_id>', methods=['PUT'])
@token_required
def update_user(user_id):
    data = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("UPDATE users SET name = %s, email = %s WHERE user_id = %s", (data["name"], data["email"], user_id))
    conn.commit()
    
    cursor.close()
    conn.close()
    return jsonify({"message": "User updated"})


# Endpoint to add a new user
@app.route('/users', methods=['POST'])
@token_required
def add_user():
    data = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (data["name"], data["email"]))
    conn.commit()
    new_user_id = cursor.lastrowid
    
    cursor.close()
    conn.close()
    return jsonify({"message": "User added", "user": {"id": new_user_id, "name": data["name"], "email": data["email"]}}), 201


if __name__ == '__main__':
    app.run(debug=True)