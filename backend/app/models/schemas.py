from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ConversationSchema(BaseModel):
    id: int
    phone_number: str
    message_text: str
    direction: str
    timestamp: datetime
    interest_score: Optional[float]
    genuine_score: Optional[float]
    decision: Optional[str]

    class Config:
        from_attributes = True