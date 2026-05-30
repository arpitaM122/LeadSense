import pickle
import pandas as pd
import os
import numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report
from xgboost import XGBClassifier
from app.core.preprocess import clean_text


def train():

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(BASE_DIR, "training_data.csv")

    print("📁 CSV Path:", csv_path)

    df = pd.read_csv(csv_path)
    df.columns = df.columns.str.strip().str.lower()

    # =========================
    # LABEL ENCODING
    # =========================
    le_interest = LabelEncoder()
    df["interest_level"] = le_interest.fit_transform(df["interest_level"].astype(str))

    df["genuine_customer"] = (
        df["genuine_customer"]
        .astype(str)
        .str.lower()
        .map({"true": 1, "false": 0, "yes": 1, "no": 0})
        .fillna(0)
        .astype(int)
    )

    # =========================
    # TEXT CLEANING
    # =========================
    df["clean_message"] = df["message"].astype(str).apply(clean_text)

    X = df["clean_message"]
    y_interest = df["interest_level"]
    y_genuine = df["genuine_customer"]

    # =========================
    # STRATIFIED SPLIT (IMPORTANT FIX)
    # =========================
    X_train_text, X_test_text, y_train_i, y_test_i, y_train_g, y_test_g = train_test_split(
        X,
        y_interest,
        y_genuine,
        test_size=0.25,
        random_state=42,
        stratify=y_interest
    )

    # =========================
    # TF-IDF (REDUCED POWER = LESS OVERFITTING)
    # =========================
    vectorizer = TfidfVectorizer(
        max_features=1000,   # reduced further
        ngram_range=(1, 1),  # REMOVE bigram memory
        min_df=5             # ignore rare words
    )

    X_train = vectorizer.fit_transform(X_train_text)
    X_test = vectorizer.transform(X_test_text)

    # =========================
    # STRONGER REGULARIZATION
    # =========================
    model_interest = XGBClassifier(
        max_depth=3,
        n_estimators=60,
        learning_rate=0.05,
        subsample=0.7,
        colsample_bytree=0.7,
        reg_lambda=2,
        reg_alpha=1,
        eval_metric="mlogloss",
        random_state=42
    )

    model_genuine = XGBClassifier(
        max_depth=3,
        n_estimators=60,
        learning_rate=0.05,
        subsample=0.7,
        colsample_bytree=0.7,
        reg_lambda=2,
        reg_alpha=1,
        eval_metric="logloss",
        random_state=42
    )

    model_interest.fit(X_train, y_train_i)
    model_genuine.fit(X_train, y_train_g)

    # =========================
    # EVALUATION
    # =========================
    print("\n==============================")
    print("📊 INTEREST MODEL REPORT")
    print("==============================")

    print(classification_report(
        y_test_i,
        model_interest.predict(X_test),
        digits=3
    ))

    print("\n==============================")
    print("📊 GENUINE MODEL REPORT")
    print("==============================")

    print(classification_report(
        y_test_g,
        model_genuine.predict(X_test),
        digits=3
    ))

    # =========================
    # SAVE
    # =========================
    artifacts_path = os.path.join(BASE_DIR, "artifacts")
    os.makedirs(artifacts_path, exist_ok=True)

    pickle.dump(model_interest, open(os.path.join(artifacts_path, "interest.pkl"), "wb"))
    pickle.dump(model_genuine, open(os.path.join(artifacts_path, "genuine.pkl"), "wb"))
    pickle.dump(vectorizer, open(os.path.join(artifacts_path, "vectorizer.pkl"), "wb"))
    pickle.dump(le_interest, open(os.path.join(artifacts_path, "label_encoder.pkl"), "wb"))

    print("\n✅ Training completed!")


if __name__ == "__main__":
    train()