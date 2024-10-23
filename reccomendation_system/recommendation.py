import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from pymongo import MongoClient


def connect_to_mongodb(uri:str = 'mongodb://localhost:27017/', db_name:str = 'article_database'):
    """Connect to the MongoDB database."""
    client = MongoClient(uri)
    return client[db_name]
def load_articles(db):
    """Load articles from the MongoDB collection."""
    articles_collection = db['articles']
    return pd.DataFrame(list(articles_collection.find()))
def load_user_preferences(db):
    """Load user preferences from the MongoDB collection."""
    labeled_articles_collection = db['labeled_articles']
    return pd.DataFrame(list(labeled_articles_collection.find()))
def generate_user_item_matrix(user_preferences_df):
    """Create a user-item matrix from user preferences."""
    user_item_matrix = user_preferences_df.pivot(index='user_id', columns='_id', values='preference')
    user_item_matrix.fillna(0, inplace=True)
    return user_item_matrix

def calculate_item_similarity(user_item_matrix):
    """Calculate item similarity matrix."""
    item_similarity = cosine_similarity(user_item_matrix.T)  # Transpose to get items as rows
    return pd.DataFrame(item_similarity, index=user_item_matrix.columns, columns=user_item_matrix.columns)


def get_recommendations(item_similarity_df, article_id, num_recommendations=5):
    """Get article recommendations based on item similarity."""
    if article_id not in item_similarity_df.columns:
        return f"Article ID {article_id} not found."

    similar_articles = item_similarity_df[article_id].sort_values(ascending=False)
    return similar_articles.index[1:num_recommendations + 1].tolist()


def main():
    # Connect to MongoDB
    db = connect_to_mongodb()
    collection = db['labeled_articles']
    documents = collection.find()
    ids=[doc['_id'] for doc in documents]
    print(ids)

    # Load data
    articles_df = load_articles(db)
    user_preferences_df = load_user_preferences(db)


    # Create user-item matrix
    user_item_matrix = generate_user_item_matrix(user_preferences_df)

    # Calculate item similarity
    item_similarity_df = calculate_item_similarity(user_item_matrix)
    #print(user_item_matrix)
    #print(item_similarity_df)
    # Example of getting recommendations for a specific article ID
    print()
    recommended_articles = get_recommendations(item_similarity_df, article_id=ids[0], num_recommendations=2)  # Replace with an actual article ID
    print(f"Recommended articles for article ID: {recommended_articles}")


if __name__ == "__main__":
    main()