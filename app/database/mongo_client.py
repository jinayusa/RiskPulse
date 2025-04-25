from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017')  # Ensure this is correct for local MongoDB
db = client['riskpulse_db']  # Database name
transactions_collection = db['transactions']  # Collection name
