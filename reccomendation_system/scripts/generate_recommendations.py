import torch

def generate_recommendations(model, user_embeddings, article_embeddings, top_n=10):
    """
    Generate article recommendations
    """
    model.eval()  # Set the model to evaluation mode

    # Predict the preferences (ratings) for all articles
    with torch.no_grad():
        predicted_preferences = model(user_embeddings, article_embeddings)

    # Get predicted preferences for all articles (article-user pairs)
    predicted_values = predicted_preferences[0]  # For the only user

    # Sort the articles based on predicted preference (highest to lowest)
    ranked_articles = torch.argsort(predicted_values, descending=True)

    # Return the top N articles
    top_articles = ranked_articles[:top_n]
    return top_articles

