from sqlalchemy.orm import Session
from app.models.database import Conversation

def record_human_feedback(conversation_id: int, correct_label: str, db: Session):
    conv = db.query(Conversation).get(conversation_id)
    if conv:
        conv.human_feedback = correct_label
        db.commit()
        # Optionally, also update Lead status if needed