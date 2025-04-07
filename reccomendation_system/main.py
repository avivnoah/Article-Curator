from mongo_repository import load_articles_from_mongodb
from scripts.preprocessing import prepare_dataloader
import pandas as pd
from models.recommendation_model import MatrixFactorizationModel, train_model
import torch
from torch.utils.data import DataLoader, TensorDataset
import joblib
from models.model_evaluation import evaluate_model
from scripts.generate_recommendations import generate_recommendations

IS_MODEL_READY = False
TO_TRAIN_MODEL = False

def save_model(model):
    model_filename = './recommendation_model.pkl'
    joblib.dump(model, model_filename)
    print("Model saved!")

def load_model(model_filename):
    """
    expecting a pkl file
    """
    model = joblib.load(model_filename)
    #print("We have loaded a model with the following parameters:")
    #print(model.params)
    return model

def main():
    if IS_MODEL_READY:
        model = load_model(model_filename="recommendation_model.pkl")
        print("loaded model")

    # Step 1: Load data from MongoDB
    data_df = load_articles_from_mongodb(uri="mongodb://localhost:27017",
                                        database_name="article_database",
                                        collection_name="labeled_articles")

    # Step 2: Prepare DataLoader
    dataloader, id_to_index, index_to_id = prepare_dataloader(data_df, batch_size=32)
    # Step 3: Train the model
    num_articles = len(id_to_index)  # Number of unique articles
    embedding_dim = 50  # Set embedding dimension

    # Train the model using the DataLoader
    model = train_model(dataloader, num_articles=num_articles, embedding_dim=embedding_dim, epochs=100000, lr=0.01)

main()