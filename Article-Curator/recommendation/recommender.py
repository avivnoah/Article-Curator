import recommender_repository
import numpy as np
from sklearn.model_selection import KFold
import tensorflow as tf
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.metrics.pairwise import cosine_similarity



def build_model(data_dim):
    model = tf.keras.models.Sequential([
        # Add an input layer
        tf.keras.layers.Dense(128, input_shape=(data_dim,), activation="relu"),
        # Add dropout to prevent overfitting
        tf.keras.layers.Dropout(0.3),

        # Add a hidden layers
        tf.keras.layers.Dense(64, activation="relu"),
        # Add dropout to prevent overfitting
        tf.keras.layers.Dropout(0.3),

        tf.keras.layers.Dense(32, activation="relu"),

        # Add an output layer with 1 output unit
        tf.keras.layers.Dense(1, activation="sigmoid")
    ])
    # Train neural network
    model.compile(
        optimizer="adam",
        loss="mean_squared_error",
        metrics=["mean_absolute_error"]
    )

    return model

def k_fold_cross_validate(data, labels, build_model_func, k=5, epochs=15, batch_size=16):
    kf = KFold(n_splits=k, shuffle=True, random_state=42)

    mae_list, mse_list, r2_list = [], [], []
    print("starting kfold")

    for fold, (train_idx, val_idx) in enumerate(kf.split(data), start=1):
        print(f"\n🔁 Fold {fold}/{k}")

        X_train, X_val = data[train_idx], data[val_idx]
        y_train, y_val = labels[train_idx], labels[val_idx]

        model = build_model_func(data.shape[1])
        model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, verbose=0)

        y_pred = model.predict(X_val).flatten()

        mae = mean_absolute_error(y_val, y_pred)
        mse = mean_squared_error(y_val, y_pred)
        r2 = r2_score(y_val, y_pred)

        mae_list.append(mae)
        mse_list.append(mse)
        r2_list.append(r2)

        print(f"MAE: {mae:.4f} | MSE: {mse:.4f} | R²: {r2:.4f}")

    print("\n📊 Cross-Validation Results:")
    print(f"Avg MAE: {np.mean(mae_list):.4f}")
    print(f"Avg MSE: {np.mean(mse_list):.4f}")
    print(f"Avg R² : {np.mean(r2_list):.4f}")

    return {
        "mae_per_fold": mae_list,
        "mse_per_fold": mse_list,
        "r2_per_fold": r2_list,
        "avg_mae": np.mean(mae_list),
        "avg_mse": np.mean(mse_list),
        "avg_r2": np.mean(r2_list)
    }
def train_model(model, collection_df=recommender_repository.load_collection(), epochs=15, batch_size=16, verbose=1):
    # For training
    data = np.stack(collection_df["vector"])  # (n_samples, 300)
    labels = collection_df["label"].values  # (n_samples,)
    history = model.fit(data, labels, epochs=epochs, batch_size=batch_size, verbose=verbose)
    print(history)
    model.save("article_preference_model2.keras")

def load_model(model_filename):
    return tf.keras.models.load_model(model_filename)

def score_model(model):
    unlabeled_collection_df = recommender_repository.load_collection(collection_name="unlabeled_articles", labeled=False)
    unlabeled_data = np.stack(unlabeled_collection_df["vector"])  # (n_samples, 300)
    unlabeled_urls = unlabeled_collection_df["url"].values  # (n_samples,)
    scores = model.predict(unlabeled_data).flatten()
    ranked = list(zip(unlabeled_urls, scores))
    recommender_repository.score_articles_in_mongo(ranked)

    # This lower segment is unnecessary!
    # If i want to print here:
    ranked.sort(key=lambda x: x[1], reverse=True)
    top_k = 5
    print("📰 Top recommended articles:")
    for i, (url, score) in enumerate(ranked[:top_k], 1):
        print(f"{i}. ({score:.3f}) {url}")




def boost_scores_with_similarity(model_scores, new_vectors, liked_vectors, alpha=0.8, beta=0.2):
    similarity_scores = []
    for vec in new_vectors:
        if liked_vectors:
            sim = np.mean(cosine_similarity([vec], liked_vectors))
        else:
            sim = 0.0
        similarity_scores.append(sim)

    final_scores = alpha * model_scores + beta * np.array(similarity_scores)
    return final_scores

def main():
    #labeled_collection_df = recommender_repository.load_collection()
    #data = np.stack(labeled_collection_df["vector"])  # (n_samples, 300)
    #labels = (labeled_collection_df["label"].values + 1) / 2  # (n_samples,)
    #urls = labeled_collection_df["url"].values  # (n_samples,)

    #model = build_model(data_dim=data.shape[1])
    # Step 1: Run k-fold validation
    #print("🔍 Running k-fold cross-validation...")
    #metrics = k_fold_cross_validate(data, labels, build_model)

    # Step 2: Train final model
    #print("\n🧠 Training final model on all data...")
    #train_model(model, labeled_collection_df)

    model = load_model("article_preference_model_test.keras")
    score_model(model)

main()

