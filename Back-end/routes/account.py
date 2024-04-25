
from flask import Flask, request, jsonify,Blueprint
from pymongo import MongoClient
from werkzeug.security import check_password_hash, generate_password_hash
from dotenv import load_dotenv
import os
import datetime
import jwt
# Load environment variables from .env file
load_dotenv()

account = Blueprint('account', __name__)
# MongoDB connection
client = MongoClient(os.environ['DATABASE_URI'])
db = client[os.environ['DATABASE_NAME']]
users_collection = db['users']

SECRET_KEY = "your_secret_key"

def create_jwt_token(username,account_type):
    # Set the payload (claims)
    payload = {
        'username': username,
        'account_type': account_type,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # Token expiration time
    }

    # Create the JWT token
    token = token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

    return token

@account.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    # print(data)
    username = data.get('username')
    password = data.get('password')
    name = data.get('name')
    account_type = data.get('account_type')
    print(username,password,name,account_type)
    # Check if username or password is missing
    if not username or not password or not name or not account_type:
        return jsonify({'message': 'Username or password is missing!','success':False})
    # Check if the user already exists
    if users_collection.find_one({'username': username}):
        return jsonify({'message': 'Username already exists!','success':False})

    # Hash the password
    try:
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
    except Exception as e:
        print(f'Error hashing password: {e}')
        return jsonify({'message': f'Error hashing password: {e}'}), 500

    # Insert new user into MongoDB
    if account_type == 'student':
        users_collection.insert_one({
            'username': username,
            'password': hashed_password,
            'name': name,
            'account_type': account_type
        })
    elif account_type == 'teacher':
        users_collection.insert_one({
            'username': username,
            'password': hashed_password,
            'name': name,
            'account_type': account_type,
            'verified': False
        })
    else:
        return jsonify({'message': 'Invalid account type!','success':False}), 
    token=create_jwt_token(username,account_type)

    return jsonify({'message': 'User registered successfully!','success':True,'token':token}), 201


@account.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    account_type = data.get('account_type')
    print(username,password,account_type)
    if not username or not password or not account_type:
        return jsonify({'message': 'Username or password is missing!','success':False})
    try:
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
    except Exception as e:
        print(f'Error hashing password: {e}')
        return jsonify({'message': f'Error hashing password: {e}'}), 500
    # Retrieve user from MongoDB
    print(hashed_password)
    user = users_collection.find_one({'username': username})
    print(user)
    if not user:
        return jsonify({'message': 'User not found!','success':False}) 
    if not check_password_hash(user['password'], password):
        return jsonify({'message': 'Invalid password!','success':False})
    token=create_jwt_token(username,account_type)
    return jsonify({'message': 'Login successful!','success':True,'token':token}), 200

