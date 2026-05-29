import pickle
import numpy as np
from app.config import settings
from app.core.preprocess import clean_text

class LeadScorer:
    def __init__(self):
        self.model = None
        self.vectorizer = None
        try:
            with open(settings.MODEL_PATH, 'rb') as f:
                self.model = pickle.load(f)
            with open(settings.VECTORIZER_PATH, 'rb') as f:
                self.vectorizer = pickle.load(f)
            print("✅ ML models loaded successfully")
        except FileNotFoundError:
            print("⚠️ Model files not found - scoring disabled until models are trained")

    def predict(self, text: str):
        if self.model is None or self.vectorizer is None:
            return {
                "interest_score": 0.5,
                "genuine_score": 0.5,
                "confidence": 0.0
            }
        cleaned = clean_text(text)
        X = self.vectorizer.transform([cleaned])
        probs = self.model.predict_proba(X)[0]
        interest_score = float(probs[0])
        genuine_score = float(probs[1])
        confidence = float(np.max(probs))
        return {
            "interest_score": interest_score,
            "genuine_score": genuine_score,
            "confidence": confidence
        }

scorer = LeadScorer()