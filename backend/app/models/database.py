from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from datetime import datetime
from app.config import settings

Base = declarative_base()

class Conversation(Base):
    __tablename__ = "conversations"
    id = Column(Integer, primary_key=True)
    phone_number = Column(String(20), index=True)
    message_text = Column(Text)
    direction = Column(String(10))
    timestamp = Column(DateTime, default=datetime.utcnow)
    interest_score = Column(Float, nullable=True)
    genuine_score = Column(Float, nullable=True)
    confidence = Column(Float, nullable=True)
    decision = Column(String(50))
    human_feedback = Column(String(50), nullable=True)
    opted_out = Column(Boolean, default=False)

class Lead(Base):
    __tablename__ = "leads"
    id = Column(Integer, primary_key=True)
    phone_number = Column(String(20), unique=True)
    first_seen = Column(DateTime, default=datetime.utcnow)
    last_interest_score = Column(Float)
    last_genuine_score = Column(Float)
    status = Column(String(50))
    opted_out = Column(Boolean, default=False)

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()