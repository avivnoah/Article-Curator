import re
import string
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk

from gensim.models import KeyedVectors
import numpy as np

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from webcrawler_main_dir_most_recent import mongodb_repository
import pandas as pd

nltk.download('punkt_tab')
nltk.download('stopwords')
nltk.download('wordnet')

STOPWORDS = stopwords.words('english')
LEMMATIZER = WordNetLemmatizer()
def clean_tokenize_article_text(text: str):
    def is_valid_token(token):
        return len(token) > 1 and not token.isnumeric()

    tokens = word_tokenize(text.lower().strip())
    split_tokens = [re.split(r"[^\w\s]", t) if not t.isalpha() else [t] for t in tokens]
    tokens = [item for sublist in split_tokens for item in sublist if item.strip()]
    tokens = [
        LEMMATIZER.lemmatize(t)
        for t in tokens
        if is_valid_token(t) and t not in string.punctuation and t not in STOPWORDS
    ]
    return tokens

def load_word2vec_model(model_path="models/GoogleNews-vectors-negative300.bin"):
    w2v_model = KeyedVectors.load_word2vec_format(model_path, binary=True)
    return w2v_model

def transform_article_tokens_to_vectors(tokens, w2v_model):
    """
    Why we use np.mean? Turn a variable-length document into a fixed-length vector,
    while capturing the "average meaning" of the document
    and also smoothing out noisy or rare word effects
    axis=0 => mean vector across all words(row by row)
    """
    vectors = [w2v_model[word] for word in tokens if word in w2v_model]
    if not vectors:
        return np.zeros(w2v_model.vector_size)  # in case we got an empty vector
    return np.mean(vectors, axis=0)
def preprocess_mongodb_collection(collection):
    w2v_model = load_word2vec_model()

    rows = []
    for doc in collection.find({}):
        if "url" in doc and "data" in doc and "preference" in doc:
            tokens = clean_tokenize_article_text(doc["data"])
            vector = transform_article_tokens_to_vectors(tokens, w2v_model)
            rows.append({
                "url": doc["url"],
                "vector": vector,
                "label": doc["preference"]
            })
    return pd.DataFrame(rows)

def preprocess_mongodb_unlabeled_collection(collection):
    w2v_model = load_word2vec_model()

    rows = []
    for doc in collection.find({}):
        if "url" in doc and "data" in doc:
            tokens = clean_tokenize_article_text(doc["data"])
            vector = transform_article_tokens_to_vectors(tokens, w2v_model)
            rows.append({
                "url": doc["url"],
                "vector": vector
            })
    return pd.DataFrame(rows)

def load_collection(collection_name="labeled_articles", labeled=False):
    if labeled:
        return preprocess_mongodb_collection(mongodb_repository.load_collection(collection_name))
    return preprocess_mongodb_unlabeled_collection(mongodb_repository.load_collection(collection_name))
