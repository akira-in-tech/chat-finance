from flask_login import UserMixin
from flask_bcrypt import Bcrypt
from bson import ObjectId

bcrypt = Bcrypt()

class User(UserMixin):
    def __init__(self, db):
        self.collection = db['users']  # MongoDB collection
    
    # Create a new user
    def create_user(self, username, password):
        if self.collection.find_one({'username': username}):
            return {"success": False, "message": "User already exists."}
        
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user_data = {
            "username": username,
            "password": hashed_password,
        }
        self.collection.insert_one(user_data)
        return {"success": True, "message": "User created successfully."}
    
    # Authenticate user
    def authenticate_user(self, username, password):
        user = self.collection.find_one({"username": username})
        if not user:
            return {"success": False, "message": "User not found!"}
        
        if bcrypt.check_password_hash(user['password'], password):
            # Convert ObjectId to string before returning the user
            user["_id"] = str(user["_id"])  # Convert ObjectId to string
            return {"success": True, "message": "Authentication successful.", "user": user}
        else:
            return {"success": False, "message": "Invalid credentials!"}
        
    # Get user by username
    def get_user(self, username):
        user = self.collection.find_one({"username": username})
        if user:
            user["_id"] = str(user["_id"])  # Convert ObjectId to string
        return user
