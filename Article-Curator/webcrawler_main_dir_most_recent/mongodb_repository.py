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

def upload_articles_to_mongodb(url_data_map, collection_name="unlabeled_articles"):
    client = MongoClient("mongodb://localhost:27017/")  # Adjust as needed
    db = client[DATABASE_NAME]  # Name of your database
    collection = db[collection_name]  # Name of your collection

    # Prepare documents for insertion
    documents = []
    for url, data in url_data_map.items():
        documents.append({
            "url": url,
            "data": data if isinstance(data, str) else "\n".join(data),
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

def load_collection(collection_name="labeled_articles"):
    client = MongoClient("mongodb://localhost:27017/")  # Adjust as needed
    db = client[DATABASE_NAME]  # Name of your database
    collection = db[collection_name]  # Name of your collection
    return collection

def update_shared_field(field_name, new_value, collection_name="unlabeled_articles"):
    client = MongoClient("mongodb://localhost:27017/")  # Adjust as needed
    db = client[DATABASE_NAME]  # Name of your database
    collection = db[collection_name]  # Name of your collection
    for doc in collection.find({field_name: {"$exists": True}}):
        old_label = doc[field_name]
        if old_label == -1:
            collection.update_one(
                {"_id": doc["_id"]},
                {"$set": {field_name: new_value}}
            )

def find_collections():
    client = MongoClient("mongodb://localhost:27017/")  # Adjust as needed
    db = client[DATABASE_NAME]  # Name of your database
    print(db.list_collection_names())


def extract_collection_difference(collection1="", collection2="", field_to_compare_by="url"):
    client = MongoClient("mongodb://localhost:27017/")  # Adjust as needed
    db = client[DATABASE_NAME]  # Name of your database
    collection1 = db[collection1]  # Name of your collection
    collection2 = db[collection2]  # Name of your collection
    docs_to_remove = set()
    for doc in collection1.find({}):
        for doc_to_subtract in collection2.find({}):
            print(doc["url"], doc_to_subtract[field_to_compare_by])
            if doc_to_subtract[field_to_compare_by] == doc[field_to_compare_by]:
                docs_to_remove.add(doc)
    if docs_to_remove:
        docs_to_remove.delete_many({"_id": {"$in": docs_to_remove}})
        print(f"Removed {len(docs_to_remove)} duplicates.")

def remove_duplicates(filter_by_field_name, collection_name="unlabeled_articles"):
    client = MongoClient("mongodb://localhost:27017/")  # Adjust as needed
    db = client[DATABASE_NAME]  # Name of your database
    collection = db[collection_name]  # Name of your collection
    # Step 1: Find duplicates by field, keeping only the first _id for each unique field value
    seen = set()
    duplicates = []

    for doc in collection.find({}):
        url = doc['url']
        if url in seen:
            duplicates.append(doc['_id'])
        else:
            seen.add(url)
    if duplicates:
        collection.delete_many({"_id": {"$in": duplicates}})
        print(f"Removed {len(duplicates)} duplicates.")

remove_duplicates("url")
#extract_collection_difference("labeled_articles", "unlabeled_articles", "url")
#update_shared_field("preference", None)
#remove_collection_field("articles", "preference")


