import pickle
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
from app.core.preprocess import clean_text

# This script expects a CSV with columns: 'message', 'interest_label', 'genuine_label'
# Labels are 0/1. For simplicity, we train two separate models.

def train():
    df = pd.read_csv("training_data.csv")
    df['clean_message'] = df['message'].apply(clean_text)
    
    X = df['clean_message']
    y_interest = df['interest_label']
    y_genuine = df['genuine_label']
    
    vectorizer = TfidfVectorizer(max_features=5000)
    X_vec = vectorizer.fit_transform(X)
    
    X_train, X_test, y_train_i, y_test_i = train_test_split(X_vec, y_interest, test_size=0.2)
    model_interest = XGBClassifier()
    model_interest.fit(X_train, y_train_i)
    
    # Train genuine model similarly
    model_genuine = XGBClassifier()
    model_genuine.fit(X_train, y_genuine)  # using same split for demo
    
    # Save both models and vectorizer
    with open("artifacts/xgboost_interest.pkl", "wb") as f:
        pickle.dump(model_interest, f)
    with open("artifacts/xgboost_genuine.pkl", "wb") as f:
        pickle.dump(model_genuine, f)
    with open("artifacts/tfidf_vectorizer.pkl", "wb") as f:
        pickle.dump(vectorizer, f)
    
    print("Training complete. Models saved.")

if __name__ == "__main__":
    train()