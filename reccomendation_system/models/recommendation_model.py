import torch
import torch.nn as nn
import torch.optim as optim

# Define the Matrix Factorization Model
# torch.nn.Module - base class for all PyTorch models - it helps organize the layers and the forward pass of the model
# Embedding dimension = how many dimensions the dense vectors for articles and preferences will have
# experiment with different sizes (e.g., 100, 200) depending on how complex the relationships are

class MatrixFactorizationModel(nn.Module):
    def __init__(self, num_articles, embedding_dim=50):

        super(MatrixFactorizationModel, self).__init__()
        self.article_embeddings = nn.Embedding(num_articles, embedding_dim) # an embedding layer that converts
        # article IDs into dense vectors. The layer has a weight matrix of size(num_articles, embedding_dim).
        # Each row corresponds to the embedding of an article. The embeddings are learned during training.
        self.preference_embeddings = nn.Embedding(2, embedding_dim)  # 2nd embedding layer
        # for preferences (-1 and 1), which are also mapped to dense vectors of
        # the same size(embedding_dim) We map preference values to indices 0 and 1 using (preferences + 1) // 2.

    # forward method defines how the data flows through the model during the forward pass. computes the prediction
    # based on the embeddings.
    #
    def forward(self, article_indices, preferences):
        # The article_indices are passed into the article_embeddings layer.
        # This retrieves the embedding vector corresponding to each article. The shape of article_embeds will be
        # (batch_size, embedding_dim), where each row is the embedding of a particular article in the batch.
        # Assuming article_indices should be long
        # Check the range of indices
        if article_indices.min() < 0:
            print("LOWER THAN ZERO:", article_indices[article_indices < 0])

        article_embeds = self.article_embeddings(article_indices.long())
        # similar to the article embeds
        preference_embeds = self.preference_embeddings(preferences)
        scores = (article_embeds * preference_embeds).sum(dim=1)  # Dot product -
        # This score represents how much the preference (-1 or 1) aligns with the article’s embedding.
        return scores

    def predict(self, article_indices, preferences):
        # Call the forward method to get the prediction scores
        return self.forward(article_indices, preferences)

# Training Function
def train_model(dataloader, num_articles, embedding_dim=50, epochs=10, lr=0.01, criterion=nn.MSELoss()):
    """
    dataloader = The DataLoader object that provides batches of data.
    num_articles = The number of articles in the dataset.
    embedding_dim = The size of the embeddings (default: 50).
    epochs = The number of epochs (iterations over the entire dataset) for training.
    lr = The learning rate for the optimizer.
    criterion = The evaluation criterion(loss function) (default: Mean Squared Error for regression)
    """
    # Initialize model, loss function, and optimizer
    model = MatrixFactorizationModel(num_articles, embedding_dim)
    # Adam optimizer -  an efficient optimizer that adapts the learning rate during training.
    # It optimizes the parameters (embeddings) of the model.
    optimizer = optim.Adam(model.parameters(), lr=lr)

    # Training loop
    for epoch in range(epochs):
        model.train()
        total_loss = 0
        for article_indices, preferences in dataloader:
            # Adjust preferences from [-1, 1] to indices [0, 1]
            preference_indices = (preferences + 1) // 2

            # Forward pass
            predictions = model(article_indices, preference_indices.long())
            loss = criterion(predictions, preferences.float())

            # Backward pass and optimization
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            total_loss += loss.item()

        print(f"Epoch {epoch + 1}/{epochs}, Loss: {total_loss:.4f}")

    return model
