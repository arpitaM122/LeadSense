import pickle
import pandas as pd
import os

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from xgboost import XGBClassifier
from app.core.preprocess import clean_text


def train():

    # =========================
    # 1. PATH SETUP
    # =========================
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(BASE_DIR, "training_data.csv")

    print("📁 CSV Path:", csv_path)

    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"CSV not found: {csv_path}")

    # =========================
    # 2. LOAD DATA
    # =========================
    df = pd.read_csv(csv_path)

    # Clean column names
    df.columns = df.columns.str.strip().str.lower()

    print("📊 Columns:", df.columns.tolist())

    # =========================
    # 3. VALIDATE REQUIRED COLUMNS
    # =========================
    required_cols = ["message", "interest_level", "genuine_customer"]

    for col in required_cols:
        if col not in df.columns:
            raise KeyError(f"Missing column: {col}")

    # =========================
    # 4. LABEL ENCODING (FIX FOR ERROR)
    # =========================

    # interest_level: high / medium / low → 0/1/2
    le_interest = LabelEncoder()
    df["interest_level"] = le_interest.fit_transform(df["interest_level"].astype(str))

    # genuine_customer: ensure numeric
    if df["genuine_customer"].dtype == "object":
        df["genuine_customer"] = df["genuine_customer"].astype(str).str.lower().map({
            "true": 1,
            "false": 0,
            "yes": 1,
            "no": 0
        })

    df["genuine_customer"] = df["genuine_customer"].astype(int)

    # =========================
    # 5. TEXT PREPROCESSING
    # =========================
    df["clean_message"] = df["message"].astype(str).apply(clean_text)

    X = df["clean_message"]
    y_interest = df["interest_level"]
    y_genuine = df["genuine_customer"]

    # =========================
    # 6. TF-IDF VECTOR
    # =========================
    vectorizer = TfidfVectorizer(max_features=5000)
    X_vec = vectorizer.fit_transform(X)

    # =========================
    # 7. TRAIN TEST SPLIT
    # =========================
    X_train, X_test, y_train_i, y_test_i, y_train_g, y_test_g = train_test_split(
        X_vec,
        y_interest,
        y_genuine,
        test_size=0.2,
        random_state=42
    )

    # =========================
    # 8. MODELS
    # =========================
    model_interest = XGBClassifier(
        eval_metric="logloss",
        random_state=42
    )
    model_interest.fit(X_train, y_train_i)

    model_genuine = XGBClassifier(
        eval_metric="logloss",
        random_state=42
    )
    model_genuine.fit(X_train, y_train_g)

    # =========================
    # 9. SAVE ARTIFACTS
    # =========================
    artifacts_path = os.path.join(BASE_DIR, "artifacts")
    os.makedirs(artifacts_path, exist_ok=True)

    with open(os.path.join(artifacts_path, "xgboost_interest.pkl"), "wb") as f:
        pickle.dump(model_interest, f)

    with open(os.path.join(artifacts_path, "xgboost_genuine.pkl"), "wb") as f:
        pickle.dump(model_genuine, f)

    with open(os.path.join(artifacts_path, "tfidf_vectorizer.pkl"), "wb") as f:
        pickle.dump(vectorizer, f)

    with open(os.path.join(artifacts_path, "label_encoder.pkl"), "wb") as f:
        pickle.dump(le_interest, f)

    print("✅ Training complete. Models saved successfully!")


if __name__ == "__main__":
    train()