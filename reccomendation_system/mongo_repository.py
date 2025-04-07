from pymongo import MongoClient
import pandas as pd


def remove_df_duplicates(df):
    print("removed duplicates, if there were any.")
    df.drop_duplicates(subset=['article_id'], keep='first', inplace=True)
    return df


def check_for_df_duplicates(df):
    duplicates = df[df.duplicated(subset=['article_id', 'preference'], keep=False)]
    # Print duplicates if any
    if not duplicates.empty:
        print("Duplicates found:")
        print(duplicates)
    else:
        print("No duplicates found.")

def average_duplicates(df):
    return df.groupby('article_id')['preference'].mean().reset_index()

def load_articles_from_mongodb(uri, database_name, collection_name):
    """
    returns data as json, with these fields:
    article_id, preference, url
    """
    # Connect to MongoDB
    client = MongoClient(uri)
    db = client[database_name]
    collection = db[collection_name]

    # Fetch all labeled articles
    articles = collection.find({"preference": {"$in": [-1, 1]}})

    # Prepare data for training
    data = []
    for article in articles:
        data.append({
            "article_id": str(article["_id"]),
            "preference": article["preference"],
            "url": article["url"]
        })
    df = pd.DataFrame(data)
    df['article_id'] = df['url'].apply(lambda x: x.split('/')[-1])  # Adjust this if needed
    df = df[['article_id', 'preference']]  # Only keep article_id and preference columns
    df = remove_df_duplicates(df)
    check_for_df_duplicates(df)
    #print(df)
    return df
