import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import joblib

TRAINING_DATA_FILE = "training_data.csv"
MODEL_OUTPUT_FILE = "cache_model.joblib"

def train_model():
    """Loads data, trains a model, and saves it."""
    print(f"Loading training data from {TRAINING_DATA_FILE}...")
    df = pd.read_csv(TRAINING_DATA_FILE)
    print(f"Found {len(df)} training examples.")

    features = ['recency', 'frequency', 'stride']
    X = df[features]
    y = df['should_evict']

    print("Training the Decision Tree model with the 'stride' feature...")
    model = DecisionTreeClassifier(max_depth=10, random_state=42)
    model.fit(X, y)
    print("Model training complete.")

    print(f"Saving trained model to {MODEL_OUTPUT_FILE}...")
    joblib.dump(model, MODEL_OUTPUT_FILE)
    print("--- Success! Your AI model is saved. ---")

if __name__ == "__main__":
    train_model()