import os
from flask import Flask
from flask_compress import Compress
from flask_cors import CORS
from dotenv import load_dotenv
from pymongo import MongoClient

# Import routes and utilities
from routes import configure_routes

# Flask application
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
Compress(app)
load_dotenv()

# MongoDB configuration
mongo_url = os.environ.get('MONGODB_URL')
if not mongo_url:
    raise ValueError("MongoDB URL is not set in the environment variables.")

mongo_client = MongoClient(mongo_url)
db = mongo_client['cdn']

# Ensure the uploads directory exists
UPLOAD_DIRECTORY = 'uploads'
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

# Register routes
configure_routes(app, db, UPLOAD_DIRECTORY)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3002)
