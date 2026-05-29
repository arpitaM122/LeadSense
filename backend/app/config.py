import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    TWILIO_ACCOUNT_SID: str = os.getenv("TWILIO_ACCOUNT_SID", "")
    TWILIO_AUTH_TOKEN: str = os.getenv("TWILIO_AUTH_TOKEN", "")
    TWILIO_WHATSAPP_NUMBER: str = os.getenv("TWILIO_WHATSAPP_NUMBER", "")
    TWILIO_SMS_NUMBER: str = os.getenv("TWILIO_SMS_NUMBER", "")
    
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost/lead_db")
    
    MODEL_PATH: str = os.getenv("MODEL_PATH", "app/training/artifacts/xgboost_model.pkl")
    VECTORIZER_PATH: str = os.getenv("VECTORIZER_PATH", "app/training/artifacts/tfidf_vectorizer.pkl")
    
    INTEREST_HIGH_THRESHOLD: float = float(os.getenv("INTEREST_HIGH_THRESHOLD", "0.7"))
    INTEREST_MEDIUM_THRESHOLD: float = float(os.getenv("INTEREST_MEDIUM_THRESHOLD", "0.4"))
    GENUINE_THRESHOLD: float = float(os.getenv("GENUINE_THRESHOLD", "0.6"))
    CONFIDENCE_LOW_THRESHOLD: float = float(os.getenv("CONFIDENCE_LOW_THRESHOLD", "0.6"))
    
    MAX_MESSAGES_PER_HOUR: int = int(os.getenv("MAX_MESSAGES_PER_HOUR", "10"))

settings = Settings()