from app.config import settings

def decide_action(interest, genuine, confidence):
    if confidence < settings.CONFIDENCE_LOW_THRESHOLD:
        return "low_confidence", "Send to human review queue"
    
    if genuine < settings.GENUINE_THRESHOLD:
        return "spam", "Block or send FAQ only"
    
    if interest >= settings.INTEREST_HIGH_THRESHOLD:
        return "high_priority", "Connect to WhatsApp/call agent"
    elif interest >= settings.INTEREST_MEDIUM_THRESHOLD:
        return "medium_interest", "Send SMS with CTA link"
    else:
        return "low_interest", "Send single follow-up question"