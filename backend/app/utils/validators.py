from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.models.database import Conversation, Lead
from app.config import settings

def is_opted_out(phone_number: str, db: Session) -> bool:
    lead = db.query(Lead).filter(Lead.phone_number == phone_number).first()
    return lead.opted_out if lead else False

def check_rate_limit(phone_number: str, db: Session) -> bool:
    one_hour_ago = datetime.utcnow() - timedelta(hours=1)
    count = db.query(Conversation).filter(
        Conversation.phone_number == phone_number,
        Conversation.timestamp >= one_hour_ago
    ).count()
    return count < settings.MAX_MESSAGES_PER_HOUR