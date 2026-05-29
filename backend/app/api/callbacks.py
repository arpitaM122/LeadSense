from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models.database import Conversation, get_db
from app.services.feedback import record_human_feedback
from pydantic import BaseModel

router = APIRouter()

class FeedbackRequest(BaseModel):
    conversation_id: int
    correct_label: str  # e.g., "spam", "genuine_high_interest", "genuine_low_interest"

@router.post("/feedback")
def submit_feedback(feedback: FeedbackRequest, db: Session = Depends(get_db)):
    conv = db.query(Conversation).filter(Conversation.id == feedback.conversation_id).first()
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")
    record_human_feedback(conv.id, feedback.correct_label, db)
    return {"status": "recorded"}

@router.post("/unsubscribe")
def unsubscribe(phone_number: str, db: Session = Depends(get_db)):
    from app.models.database import Lead
    lead = db.query(Lead).filter(Lead.phone_number == phone_number).first()
    if lead:
        lead.opted_out = True
    else:
        lead = Lead(phone_number=phone_number, opted_out=True, status="unsubscribed")
        db.add(lead)
    db.commit()
    return {"status": "unsubscribed"}