import pandas as pd
import os
import json
import subprocess
from pymongo import MongoClient

MONGODB_ADDRESS = 'mongodb://localhost:27017/'
def stop_mongodb():
    try:
        # Stop the MongoDB service
        result = subprocess.run(['net', 'stop', 'MongoDB'], check=True, capture_output=True, text=True)
        print("MongoDB service stopped successfully!")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("Failed to stop MongoDB service.")
        print(e.stderr)
def start_mongodb():
    """
    This method runs the mongoDB server locally
    """
    try:
        # Run the 'net start MongoDB' command
        result = subprocess.run(['net', 'start', 'MongoDB'], check=True, capture_output=True, text=True)
        print("MongoDB service started successfully!")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("Failed to start MongoDB service.")
        print(e.stderr)

def upload_articles_to_mongodb(url_data_map):
    client = MongoClient("mongodb://localhost:27017/")  # Adjust as needed
    db = client["article_database"]  # Name of your database
    collection = db["articles"]  # Name of your collection

    # Prepare documents for insertion
    documents = []
    for url, data in url_data_map.items():
        documents.append({
            "url": url,
            "data": "\n".join(data)
        })
    # Insert the documents into MongoDB
    result = collection.insert_many(documents)

    # Print inserted IDs
    print(f"Inserted documents with IDs: {result.inserted_ids}")