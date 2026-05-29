from fastapi import APIRouter, Request, HTTPException, Depends
from sqlalchemy.orm import Session
from twilio.twiml.messaging_response import MessagingResponse
from app.core.lead_scoring import scorer
from app.core.decision_engine import decide_action
from app.channels.whatsapp import send_whatsapp_buttons
from app.channels.sms import send_sms
from app.services.human_queue import add_to_review_queue
from app.models.database import Conversation, Lead, get_db
from app.utils.validators import is_opted_out, check_rate_limit

router = APIRouter()

@router.post("/webhook/twilio")
async def twilio_webhook(request: Request, db: Session = Depends(get_db)):
    form_data = await request.form()
    from_number = form_data.get("From")
    body = form_data.get("Body", "").strip()
    
    # 1. Opt-out check
    if is_opted_out(from_number, db):
        resp = MessagingResponse()
        resp.message("You have unsubscribed. Reply START to opt in.")
        return str(resp)
    
    # 2. Rate limit
    if not check_rate_limit(from_number, db):
        resp = MessagingResponse()
        resp.message("Too many messages. Please try later.")
        return str(resp)
    
    # 3. Save raw message
    conv = Conversation(phone_number=from_number, message_text=body, direction="inbound")
    db.add(conv)
    db.commit()
    db.refresh(conv)
    
    # 4. AI scoring
    scores = scorer.predict(body)
    conv.interest_score = scores["interest_score"]
    conv.genuine_score = scores["genuine_score"]
    conv.confidence = scores["confidence"]
    db.commit()
    
    # 5. Decision
    action, reason = decide_action(
        scores["interest_score"],
        scores["genuine_score"],
        scores["confidence"]
    )
    conv.decision = action
    db.commit()
    
    # 6. Take action
    if action == "low_confidence":
        add_to_review_queue(from_number, body, scores, db)
        reply = "Thank you. A human will review your query shortly."
    
    elif action == "spam":
        reply = "We couldn't process your request. Please contact support@example.com"
    
    elif action == "high_priority":
        send_whatsapp_buttons(from_number, ["Talk to agent", "Schedule a call"])
        reply = "You're a high-priority lead! Choose an option below."
    
    elif action == "medium_interest":
        send_sms(from_number, "Reply YES to get a callback from our sales team.")
        reply = "We'll be in touch shortly."
    
    else:  # low_interest
        reply = "Thanks for reaching out. Let us know if you have any specific questions."
    
    # Send reply via same channel (inbound channel detection simplified)
    resp = MessagingResponse()
    resp.message(reply)
    return str(resp)