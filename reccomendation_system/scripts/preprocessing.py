import torch
from torch.utils.data import Dataset, DataLoader

# Map article IDs to numeric indices
# creating map and reverse map:
def create_article_mapping(df):
    article_ids = df['article_id'].unique()  # Extract unique article_ids from the DataFrame
    id_to_index = {article_id: idx for idx, article_id in enumerate(article_ids)}
    index_to_id = {idx: article_id for article_id, idx in id_to_index.items()}
    return id_to_index, index_to_id

# Define a custom Dataset:
# Stores the list of articles and the id_to_index mapping
# converts article IDd to the numeric index,
# Returns (article_index, preference) as a pytorch tensor for model training
class ArticlePreferenceDataset(Dataset):
    def __init__(self, df, id_to_index):
        """
        Args:
            df (pandas.DataFrame): DataFrame containing 'article_id' and 'preference'.
            id_to_index (dict): Mapping of article IDs to indices.
        """
        self.df = df
        self.id_to_index = id_to_index

    def __len__(self):
        return len(self.df)

    def __getitem__(self, idx):
        article_id = self.df.iloc[idx]['article_id']
        preference = self.df.iloc[idx]['preference']
        article_index = self.id_to_index[article_id]
        return torch.tensor(article_index, dtype=torch.long), torch.tensor(preference, dtype=torch.float)

# Create DataLoaders:
# Splits the data into batches, which are essential for efficient training
# handles shuffling, to prevent the model from memorizing the order of samples.

def prepare_dataloader(df, batch_size=32):
    # Create the article to index mapping using the DataFrame
    id_to_index, index_to_id = create_article_mapping(df)

    # Create the dataset from the DataFrame
    dataset = ArticlePreferenceDataset(df, id_to_index)

    # Create the DataLoader
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

    return dataloader, id_to_index, index_to_id

