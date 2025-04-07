import pandas as pd
import os
import json
import subprocess
from pymongo import MongoClient

DATABASE_NAME = "article_database"
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
    db = client[DATABASE_NAME]  # Name of your database
    collection = db["articles"]  # Name of your collection

    # Prepare documents for insertion
    documents = []
    for url, data in url_data_map.items():
        documents.append({
            "url": url,
            "data": "\n".join(data),
            "user_id": 1,
            "preference": 0
        })
    # Insert the documents into MongoDB
    result = collection.insert_many(documents)

    # Print inserted IDs
    print(f"Inserted documents with IDs: {result.inserted_ids}")

def duplicate_collection(source_collection_name, output_collection_name):
    """
    Assuming the collection doesn't exist yet!
    :param source_collection_name:
    :param output_collection_name:
    """
    client = MongoClient("mongodb://localhost:27017/")  # Adjust as needed
    db = client[DATABASE_NAME]  # Name of your database
    source_collection = db[source_collection_name]  # Name of your collection
    new_collection = db[output_collection_name] # Name of your new collection

    # Copy all documents from the source collection to the new collection
    documents = source_collection.find()
    # Insert documents into the new collection
    new_collection.insert_many(documents)
    print(f"Collection '{source_collection_name}' duplicated to '{output_collection_name}' in database '{DATABASE_NAME}'.")

def remove_collection_field(collection_name, field_name):
    """
    removes from all items in the dataset
    """
    client = MongoClient("mongodb://localhost:27017/")  # Adjust as needed
    db = client[DATABASE_NAME]  # Name of your database
    collection = db[collection_name]  # Name of your collection
    result = collection.update_many({}, {'$unset': {field_name: ""}})
    print(f"Removed field '{field_name}' from {result.modified_count} documents in collection '{collection_name}'.")
def add_collection_field(collection_name, field_name, value):
    """
    adds to all items in the dataset
    """
    client = MongoClient("mongodb://localhost:27017/")  # Adjust as needed
    db = client[DATABASE_NAME]  # Name of your database
    collection = db[collection_name]  # Name of your collection
    result = collection.update_many({}, {'$set': {field_name: value}})
    print(f"Added field '{field_name}' with value '{value}' to {result.modified_count} documents in collection '{collection_name}'.")

remove_collection_field("articles", "preference")


