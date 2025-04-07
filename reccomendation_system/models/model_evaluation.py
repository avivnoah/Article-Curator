import torch
import torch.nn.functional as F
import numpy as np
# Assuming your model, user embeddings, article embeddings, and data are already loaded

# Step 1: Define a function to calculate Mean Squared Error (MSE)
def evaluate_model(model, user_embeddings, article_embeddings, true_preferences, indices):
    model.eval()  # Set the model to evaluation mode - disables dropout and batch normalization

    # Predict the preferences (ratings) for all articles
    with torch.no_grad():
        predicted_preferences = model(user_embeddings, article_embeddings)

    # Extract the predicted preferences for the relevant article-user pairs
    predicted_values = predicted_preferences[indices[:, 0], indices[:, 1]]

    # Calculate MSE by comparing true preferences with predicted values
    mse = F.mse_loss(predicted_values, true_preferences)
    return mse.item()

