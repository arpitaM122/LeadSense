from sqlalchemy.orm import Session
from app.models.database import Conversation

def add_to_review_queue(phone_number: str, message: str, scores: dict, db: Session):
    # Create a special conversation entry flagged for review
    conv = Conversation(
        phone_number=phone_number,
        message_text=message,
        direction="inbound",
        decision="low_confidence",
        interest_score=scores["interest_score"],
        genuine_score=scores["genuine_score"],
        confidence=scores["confidence"]
    )
    db.add(conv)
    db.commit()
    # In production, also push to a Redis queue or notify Slack